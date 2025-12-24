from abc import ABC, abstractmethod


class BaseCalculation(ABC):
    @abstractmethod
    def calculate(self, data: dict) -> dict:
        pass
