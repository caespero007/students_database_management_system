from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str
    age: int
    course: str
    year: int
    marks: int


class StudentUpdate(BaseModel):
    name: str
    email: str
    age: int
    course: str
    year: int
    marks: int


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    course: str
    year: int
    marks: int

    class Config:
        from_attributes = True


class AIRequest(BaseModel):
    question: str