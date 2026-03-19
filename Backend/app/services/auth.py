"""
Firebase authentication and JWT verification.
"""

import os
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends, Request
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase (requires FIREBASE_CREDENTIALS_JSON environment variable)
FIREBASE_CREDENTIALS_JSON = os.getenv("FIREBASE_CREDENTIALS_JSON")
FIREBASE_ENABLED = False

if FIREBASE_CREDENTIALS_JSON:
    try:
        # Try to initialize Firebase if credentials are provided
        if not firebase_admin._apps:
            creds = credentials.Certificate(FIREBASE_CREDENTIALS_JSON)
            firebase_admin.initialize_app(creds)
            FIREBASE_ENABLED = True
            print("[v0] Firebase initialized successfully")
    except Exception as e:
        print(f"[v0] Warning: Could not initialize Firebase: {e}")
        print("[v0] Firebase auth will be disabled. Use FIREBASE_CREDENTIALS_JSON to enable it.")
else:
    print("[v0] Firebase credentials not found. Auth will be disabled - all endpoints are public.")


class AuthService:
    """Service for Firebase authentication and token verification"""
    
    @staticmethod
    def extract_token_from_header(request: Request) -> Optional[str]:
        """
        Extract JWT token from Authorization header.
        
        Args:
            request: FastAPI request object
        
        Returns:
            Token string or None if not present
        """
        auth_header = request.headers.get("authorization")
        if not auth_header:
            return None
        
        # Expected format: "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        
        return parts[1]
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase JWT token. If Firebase is disabled, returns None.
        
        Args:
            token: Firebase JWT token from Authorization header
        
        Returns:
            Decoded token claims if valid, None if invalid
        """
        try:
            # If Firebase is disabled, skip verification
            if not FIREBASE_ENABLED:
                return None
            
            # Verify the token
            decoded_token = firebase_auth.verify_id_token(token)
            return decoded_token
        
        except firebase_auth.ExpiredIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except firebase_auth.InvalidIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification failed: {str(e)}"
            )
    
    @staticmethod
    def get_user_from_token(decoded_token: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract user information from decoded Firebase token.
        
        Args:
            decoded_token: Decoded JWT token from Firebase
        
        Returns:
            Dictionary with user_id, email, and other user info
        """
        return {
            "user_id": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "display_name": decoded_token.get("name"),
            "email_verified": decoded_token.get("email_verified", False),
            "iat": decoded_token.get("iat"),  # Issued at
            "exp": decoded_token.get("exp"),  # Expiration
        }


async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Dependency for FastAPI to extract and verify current user from JWT.
    
    Usage:
        @app.post("/api/calculate/emi")
        async def emi_endpoint(
            request: EMIRequest,
            current_user: Dict = Depends(get_current_user)
        ):
            # current_user contains: user_id, email, etc.
            pass
    """
    token = AuthService.extract_token_from_header(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    decoded_token = AuthService.verify_token(token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return decoded_token


async def get_current_user_optional(request: Request) -> Optional[Dict[str, Any]]:
    """
    Optional authentication dependency.
    Allows unauthenticated requests but provides user info if token is present.
    
    Usage:
        @app.post("/api/calculate/emi")
        async def emi_endpoint(
            request: EMIRequest,
            current_user: Optional[Dict] = Depends(get_current_user_optional)
        ):
            # current_user is None if no token provided
            pass
    """
    token = AuthService.extract_token_from_header(request)
    if not token:
        return None
    
    try:
        return AuthService.verify_token(token)
    except HTTPException:
        # If verification fails, return None instead of raising
        return None
