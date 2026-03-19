"""
SQLAlchemy ORM models for calculation history and user data.
"""

from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model - stores basic user information from Firebase"""
    __tablename__ = "users"
    
    user_id = Column(String(255), primary_key=True, index=True)  # Firebase UID
    email = Column(String(255), unique=True, index=True)
    display_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CalculationHistory(Base):
    """Model to store calculation history for audit and analytics"""
    __tablename__ = "calculation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)  # User who performed calculation
    
    calculator_type = Column(String(50), index=True)  # e.g., "emi", "sip", "cagr"
    calculator_name = Column(String(100))  # e.g., "EMI Calculator", "SIP Calculator"
    calculator_version = Column(String(10), default="1.0")
    
    # Input parameters stored as JSON
    inputs = Column(JSON)
    
    # Calculation results stored as JSON
    result = Column(JSON)
    
    # Additional metadata
    formula = Column(Text, nullable=True)
    assumptions = Column(JSON, nullable=True)
    
    # Timestamps for audit trail
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CalculationHistory(user_id={self.user_id}, calculator_type={self.calculator_type}, created_at={self.created_at})>"


class CalculationTemplate(Base):
    """Model to store user-created calculation templates/scenarios"""
    __tablename__ = "calculation_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    
    template_name = Column(String(255))
    calculator_type = Column(String(50), index=True)
    
    # Template parameters as JSON
    template_inputs = Column(JSON)
    
    # Notes/description
    description = Column(Text, nullable=True)
    
    # Is default/favorite
    is_favorite = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CalculationTemplate(user_id={self.user_id}, template_name={self.template_name})>"


class QuickNotes(Base):
    """Model to store user notes/insights related to calculations"""
    __tablename__ = "quick_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    
    calculation_history_id = Column(Integer, nullable=True)  # Link to specific calculation
    
    note_text = Column(Text)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<QuickNotes(user_id={self.user_id}, id={self.id})>"
