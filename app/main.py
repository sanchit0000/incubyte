from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employees/", response_model=schemas.Employee, status_code=201)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = models.Employee(**employee.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


@app.get("/employees/{emp_id}", response_model=schemas.Employee)
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@app.put("/employees/{emp_id}", response_model=schemas.Employee)
def update_employee(
    emp_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)
):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.model_dump().items():
        setattr(db_emp, key, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp


@app.delete("/employees/{emp_id}", status_code=204)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_emp)
    db.commit()
    return Response(status_code=204)


@app.get("/employees/{emp_id}/salary")
def get_salary_info(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    tax_map = {"India": 0.10, "United States": 0.12}
    tax_rate = tax_map.get(emp.country, 0.0)
    deductions = emp.salary * tax_rate

    return {
        "gross_salary": emp.salary,
        "deductions": deductions,
        "net_salary": emp.salary - deductions,
    }


@app.get("/metrics/country/{country}")
def get_country_metrics(country: str, db: Session = Depends(get_db)):
    stats = (
        db.query(
            func.min(models.Employee.salary),
            func.max(models.Employee.salary),
            func.avg(models.Employee.salary),
        )
        .filter(models.Employee.country == country)
        .first()
    )

    if stats[0] is None:
        raise HTTPException(status_code=404, detail="No data for this country")

    return {"min": stats[0], "max": stats[1], "avg": stats[2]}


@app.get("/metrics/job-title/{job_title}")
def get_job_metrics(job_title: str, db: Session = Depends(get_db)):
    avg = (
        db.query(func.avg(models.Employee.salary))
        .filter(models.Employee.job_title == job_title)
        .scalar()
    )
    if avg is None:
        raise HTTPException(status_code=404, detail="Job title not found")
    return {"job_title": job_title, "average_salary": avg}
