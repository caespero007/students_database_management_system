from sqlalchemy.orm import Session
from sqlalchemy import or_

from .models import Student
from .schemas import StudentCreate, StudentUpdate


# CREATE
def create_student(db: Session, student: StudentCreate):

    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age,
        course=student.course,
        year=student.year,
        marks=student.marks
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# READ ALL
def get_students(db: Session):

    return db.query(Student).order_by(Student.id.desc()).all()


# READ ONE
def get_student(db: Session, student_id: int):

    return db.query(Student).filter(
        Student.id == student_id
    ).first()


# SEARCH
def search_students(db: Session, query: str):

    return db.query(Student).filter(
        or_(
            Student.name.ilike(f"%{query}%"),
            Student.email.ilike(f"%{query}%"),
            Student.course.ilike(f"%{query}%")
        )
    ).all()


# UPDATE
def update_student(
    db: Session,
    student_id: int,
    student: StudentUpdate
):

    existing_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not existing_student:
        return None

    existing_student.name = student.name
    existing_student.email = student.email
    existing_student.age = student.age
    existing_student.course = student.course
    existing_student.year = student.year
    existing_student.marks = student.marks

    db.commit()
    db.refresh(existing_student)

    return existing_student


# DELETE
def delete_student(db: Session, student_id: int):

    existing_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not existing_student:
        return None

    db.delete(existing_student)
    db.commit()

    return existing_student


# STATISTICS
def get_statistics(db: Session):

    students = db.query(Student).all()

    total = len(students)

    if total == 0:

        return {
            "total_students": 0,
            "average_marks": 0,
            "average_age": 0,
            "highest_marks": 0,
            "top_student": None
        }

    average_marks = sum(
        student.marks for student in students
    ) / total

    average_age = sum(
        student.age for student in students
    ) / total

    top_student = max(
        students,
        key=lambda student: student.marks
    )

    return {
        "total_students": total,
        "average_marks": round(average_marks, 2),
        "average_age": round(average_age, 2),
        "highest_marks": top_student.marks,
        "top_student": top_student.name
    }