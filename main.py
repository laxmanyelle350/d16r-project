from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import crud
import schemas

from database import Base, engine, SessionLocal
from auth import verify_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user, db)

@app.post("/login")
def login(
    response: Response,
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    return crud.login_user(user, db, response)


@app.post("/students", response_model=schemas.StudentResponse)
def add_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)


@app.get("/students", response_model=list[schemas.StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    user=Depends(verify_admin)
):
    return crud.get_students(db)



@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def search_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    return student


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):

    updated = crud.update_student(
        db,
        student_id,
        student
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    return updated


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    deleted = crud.delete_student(
        db,
        student_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    return {
        "message": "Student Deleted Successfully"
    }


@app.get("/branch/{branch}")
def branch_students(
    branch: str,
    db: Session = Depends(get_db)
):
    return crud.get_student_by_branch(
        db,
        branch
    )


@app.get("/total/{student_id}")
def total(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.total_marks(
        db,
        student_id
    )

@app.get("/percentage/{student_id}")
def percentage(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.percentage(
        db,
        student_id
    )


@app.get("/grade/{student_id}")
def grade(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.grade(
        db,
        student_id
    )


@app.get("/topper")
def topper(
    db: Session = Depends(get_db)
):
    return crud.topper(db)