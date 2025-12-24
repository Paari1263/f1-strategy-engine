from pydantic import BaseModel

class DriverBase(BaseModel):
    driver_number: int
