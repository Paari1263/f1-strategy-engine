"""
Base Calculation Interface
Abstract base class for all mathematical calculations
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel


class BaseCalculation(ABC):
    """
    Abstract base class for all calculation modules.
    All calculations must be pure functions with no side effects.
    """
    
    @abstractmethod
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Perform the calculation and return results.
        
        Args:
            **kwargs: Calculation-specific input parameters
            
        Returns:
            Dict containing calculation results
        """
        pass
    
    def validate_inputs(self, **kwargs) -> bool:
        """
        Validate input parameters before calculation.
        
        Args:
            **kwargs: Input parameters to validate
            
        Returns:
            True if inputs are valid, False otherwise
        """
        return True
    
    @property
    @abstractmethod
    def calculation_name(self) -> str:
        """Return unique identifier for this calculation"""
        pass
    
    @property
    def description(self) -> str:
        """Return human-readable description of calculation"""
        return f"{self.calculation_name} calculation"
    
    def __call__(self, **kwargs) -> Dict[str, Any]:
        """
        Make calculation callable as a function.
        Validates inputs before executing calculation.
        """
        if not self.validate_inputs(**kwargs):
            raise ValueError(f"Invalid inputs for {self.calculation_name}")
        return self.calculate(**kwargs)


class CalculationResult(BaseModel):
    """Base model for calculation results"""
    calculation_name: str
    value: Any
    unit: Optional[str] = None
    confidence: Optional[float] = None  # 0.0 to 1.0
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        arbitrary_types_allowed = True
