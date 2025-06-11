from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClimateHistoryBase(BaseModel):
    temperature: Optional[float] = None
    humidity:    Optional[float] = None
    light_intensity: Optional[float] = None
    record_date: datetime
    shop_id: int

class ClimateHistoryCreate(ClimateHistoryBase):
    pass

class ClimateHistoryUpdate(ClimateHistoryBase):
    pass

class ClimateHistory(ClimateHistoryBase):
    climate_history_id: int

    model_config = {
        "from_attributes": True
    }
