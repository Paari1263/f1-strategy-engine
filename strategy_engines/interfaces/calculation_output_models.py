from dataclasses import dataclass


@dataclass
class CalculationResult:
    name: str
    metrics: dict
