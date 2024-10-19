from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    admin = "admin"
    reviewer = "reviewer"
    digitizer = "digitizer"

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: UserRole


class UserUpdateRole(BaseModel):
    role: UserRole

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True  # Вместо orm_mode



# Схема для создания нового лога
class LogCreate(BaseModel):
    api: str
    image_type: str
    digitization_scale: str
    scale_type: str
    depth_start: float
    depth_end: float
    trajectory: bool
    logs: str
    digitized_logs: str

# Схема для обновления существующего лога
class LogUpdate(BaseModel):
    api: Optional[str] = None
    image_type: Optional[str] = None
    digitization_scale: Optional[str] = None
    scale_type: Optional[str] = None
    depth_start: Optional[float] = None
    depth_end: Optional[float] = None
    trajectory: Optional[bool] = None
    logs: Optional[str] = None
    digitized_logs: Optional[str] = None
    assigned_to: Optional[int] = None  # ID пользователя, которому назначена запись


# Схема для вывода информации о логе
class LogOut(BaseModel):
    id: int
    api: str
    image_type: str
    digitization_scale: str
    scale_type: str
    depth_start: float
    depth_end: float
    trajectory: bool
    logs: str
    digitized_logs: str
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }