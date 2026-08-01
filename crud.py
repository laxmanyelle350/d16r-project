from sqlalchemy.orm import Session
import models
import schemas
import bcrypt
from datetime import datetime, timedelta
import jwt
from fastapi import Response
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_student(db: Session, student: schemas.StudentCreate):

    db_student = models.Student(**student.model_dump())

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def create_user(user: schemas.UserCreate, db: Session):
    new_user = models.Users(**user.model_dump())

    hashed = bcrypt.hashpw(
        new_user.password.encode(),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user.password = hashed

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_students(db: Session):
    return db.query(models.Student).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()
    
    
def update_student(db: Session, student_id: int, student: schemas.StudentCreate):

    db_student = get_student(db, student_id)

    if not db_student:
        return None

    db_student.name = student.name
    db_student.branch = student.branch

    db_student.marks1 = student.marks1
    db_student.marks2 = student.marks2
    db_student.marks3 = student.marks3

    db_student.email = student.email
    db_student.phone = student.phone

    db.commit()
    db.refresh(db_student)

    return db_student



def delete_student(db: Session, student_id: int):

    db_student = get_student(db, student_id)

    if not db_student:
        return None
    

    db.delete(db_student)
    db.commit()

    return db_student


def get_student_by_branch(db: Session, branch: str):

    return db.query(models.Student).filter(
        models.Student.branch == branch
    ).all()
    
    
    
def total_marks(db: Session, student_id: int):

    student = get_student(db, student_id)

    if not student:
        return None

    total = student.marks1 + student.marks2 + student.marks3

    return {
        "student": student.name,
        "total": total
    }
    
    
def percentage(db: Session, student_id: int):

    student = get_student(db, student_id)

    if not student:
        return None

    total = student.marks1 + student.marks2 + student.marks3

    percent = total / 3

    return {
        "student": student.name,
        "percentage": percent
    }
def grade(db: Session, student_id: int):

    student = get_student(db, student_id)

    if not student:
        return None

    total = student.marks1 + student.marks2 + student.marks3

    percentage = total / 3

    if percentage >= 90:
        grade = "A+"

    elif percentage >= 80:
        grade = "A"

    elif percentage >= 70:
        grade = "B"

    elif percentage >= 60:
        grade = "C"

    elif percentage >= 35:
        grade = "D"

    else:
        grade = "Fail"

    return {
        "student": student.name,
        "grade": grade
    }
def topper(db: Session):

    students = db.query(models.Student).all()

    if not students:
        return None

    topper = max(
        students,
        key=lambda x: x.marks1 + x.marks2 + x.marks3
    )

    return topper


def login_user(user: schemas.UserLogin, db: Session, response: Response):

    is_exists = db.query(models.Users).filter(
        models.Users.email == user.email
    ).first()

    if not is_exists:
        return {"message": "User Not Found"}

    valid = bcrypt.checkpw(
        user.password.encode(),
        is_exists.password.encode()
    )

    if not valid:
        return {"message": "Invalid Password"}

    payload = {
        "name": is_exists.name,
        "email": is_exists.email,
        "is_admin": is_exists.is_admin,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return {
        "message": "Login Successful",
        "access_token": token
    }