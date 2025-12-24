from dataclasses import dataclass


@dataclass
class DriverInput:
    driver_id: int
    lap_times: list
    incidents: int
    tyre_usage: dict


@dataclass
class CarInput:
    team: str
    power: float
    aero: float
    drag: float
    reliability: float
