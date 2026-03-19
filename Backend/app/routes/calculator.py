from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.services.calculator_router import CalculatorRegistry

router = APIRouter(prefix="/api", tags=["Calculators"])


# -------------------------------
# REQUEST MODEL
# -------------------------------
class CalculateRequest(BaseModel):
    type: str
    inputs: Dict[str, Any]


# -------------------------------
# GET SINGLE CALCULATOR CONFIG
# -------------------------------
@router.get("/calculators/{calculator_type}")
def get_calculator(calculator_type: str):
    try:
        info = CalculatorRegistry.get_calculator_info(calculator_type)

        return {
            "type": calculator_type,
            "name": info["description"],
            "description": info["description"],

            # 👇 STATIC INPUT SCHEMA (IMPORTANT)
            # You can expand later
            "inputs": [
                {
                    "id": "principal",
                    "label": "Principal Amount",
                    "type": "number",
                },
                {
                    "id": "rate",
                    "label": "Interest Rate (%)",
                    "type": "number",
                },
                {
                    "id": "tenure",
                    "label": "Tenure (years)",
                    "type": "number",
                },
            ],
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------------------
# CALCULATE ENDPOINT
# -------------------------------
@router.post("/calculate")
def calculate(payload: CalculateRequest):
    try:
        result = CalculatorRegistry.execute_calculator(
            payload.type,
            payload.inputs
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))