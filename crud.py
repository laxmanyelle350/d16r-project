from sqlalchemy.orm import Session
import models
import schemas
import bcrypt

def create_student(db: Session, student: schemas.StudentCreate):

    db_student = models.Student(**student.model_dump())

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


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