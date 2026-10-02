from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import Student
from .schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    AIRequest
)
from . import crud
from .ai import ask_ai


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Student Database Management System",
    description="Student Management System with Gemini AI",
    version="1.0.0"
)


# HOME
@app.get("/")
def home():

    return {
        "message": "Student Database Management System is running",
        "docs": "/docs"
    }


# HEALTH CHECK
@app.get("/health")
def health():

    return {
        "status": "running",
        "application": "Student Database Management System"
    }


# CREATE STUDENT
@app.post(
    "/students",
    response_model=StudentResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    existing_student = db.query(Student).filter(
        Student.email == student.email
    ).first()

    if existing_student:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.create_student(db, student)


# GET ALL STUDENTS
@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):

    return crud.get_students(db)


# SEARCH STUDENTS
@app.get(
    "/search",
    response_model=list[StudentResponse]
)
def search_students(
    q: str = "",
    db: Session = Depends(get_db)
):

    if not q.strip():

        return crud.get_students(db)

    return crud.search_students(db, q)


# GET ONE STUDENT
@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = crud.get_student(
        db,
        student_id
    )

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# UPDATE STUDENT
@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):

    # Check whether email belongs to another student
    duplicate_email = db.query(Student).filter(
        Student.email == student.email,
        Student.id != student_id
    ).first()

    if duplicate_email:

        raise HTTPException(
            status_code=400,
            detail="Email already belongs to another student"
        )

    updated_student = crud.update_student(
        db,
        student_id,
        student
    )

    if not updated_student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student


# DELETE STUDENT
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    deleted_student = crud.delete_student(
        db,
        student_id
    )

    if not deleted_student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }


# STATISTICS
@app.get("/statistics")
def statistics(
    db: Session = Depends(get_db)
):

    return crud.get_statistics(db)


# AI CHATBOT
@app.post("/ai")
def ai_chat(
    request: AIRequest,
    db: Session = Depends(get_db)
):

    students = crud.get_students(db)

    answer = ask_ai(
        request.question,
        students
    )

    return {
        "question": request.question,
        "answer": answer
    }