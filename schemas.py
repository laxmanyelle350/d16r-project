from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    branch: str

    marks1: int
    marks2: int
    marks3: int

    email: str
    phone: str


class StudentResponse(StudentCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(UserCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: str
    password: str