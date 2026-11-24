from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


patients = [
    {
        "id": "a81f2c90-7b34-4d12-9e56-123456789001",
        "name": "Ahmed Khan",
        "age": 25,
        "height": 5.8,
        "weight": 72.5,
        "gender": "Male",
        "email": "ahmed@example.com",
        "phone": "+923001234567",
        "blood_group": "B+",
        "disease": "Diabetes",
        "is_admitted": True,
    },
    {
        "id": "b92e3d10-8c45-4a23-8f67-234567890012",
        "name": "Sara Ahmed",
        "age": 32,
        "height": 5.4,
        "weight": 58.0,
        "gender": "Female",
        "email": "sara@example.com",
        "phone": "+923121234567",
        "blood_group": "A+",
        "disease": "Hypertension",
        "is_admitted": False,
    },
    {
        "id": "c73d4e20-9a56-4b34-8d78-345678901023",
        "name": "Usman Ali",
        "age": 45,
        "height": 5.9,
        "weight": 85.0,
        "gender": "Male",
        "email": "usman@example.com",
        "phone": "+923331234567",
        "blood_group": "O+",
        "disease": "Asthma",
        "is_admitted": True,
    },
    {
        "id": "d64e5f30-1b67-4c45-9a89-456789012034",
        "name": "Ayesha Malik",
        "age": 28,
        "height": 5.3,
        "weight": 55.5,
        "gender": "Female",
        "email": "ayesha@example.com",
        "phone": "+923451234567",
        "blood_group": "AB+",
        "disease": "Migraine",
        "is_admitted": False,
    },
    {
        "id": "e55f6a40-2c78-4d56-8b90-567890123045",
        "name": "Bilal Hussain",
        "age": 60,
        "height": 5.7,
        "weight": 90.0,
        "gender": "Male",
        "email": "bilal@example.com",
        "phone": "+923211234567",
        "blood_group": "O-",
        "disease": "Heart Disease",
        "is_admitted": True,
    },
]


class Filters(BaseModel):
    model_config = {"extra": "forbid"}

    order: Literal["ASC", "DESC"] = Field(
        default="ASC",
        title="Sort Order",
        description="Choose ascending or descending order",
    )
    sort_by: Literal["age", "height", "weight"] | None = Field(
        default=None,
        title="Sort By",
        description="Choose which patient field to sort by",
    )


class PatientBase(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    gender: Literal["Male", "Female"]
    email: EmailStr
    phone: str
    blood_group: Literal["B+", "A+", "O+", "AB+", "B-", "A-", "O-", "AB-"]
    disease: str
    is_admitted: bool = False


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: str


class PatientListResponse(BaseModel):
    data: list[PatientResponse]
    order: Literal["ASC", "DESC"] = "ASC"
    sort_by: Literal["age", "height", "weight"] | None = None


@app.get("/patient", response_model=PatientListResponse)
def get_patients(query: Annotated[Filters, Query()]):

    if query.sort_by:
        data = sorted(
            patients,
            key=lambda patient: patient[query.sort_by],
            reverse=query.order == "DESC",
        )
    else:
        data = patients.copy()

    return {
        "data": data,
        "order": query.order,
        "sort_by": query.sort_by,
    }


@app.get("/patient/{patient_id}", response_model=PatientResponse)
def get_patients_by_id(
    patient_id: Annotated[
        str, Path(title="Patient ID", description="The unique ID of the patient")
    ],
):

    for patient in patients:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail={
            "message": "Patient not found",
            "instruction": "Please provide a valid patient ID",
        },
    )


@app.delete("/patient/{patient_id}")
def delete_patient(
    patient_id: Annotated[
        str, Path(title="Patient ID", description="The unique ID of the patient")
    ],
):

    for patient in patients:
        if patient["id"] == patient_id:
            patients.remove(patient)
            return {"message": "Patient deleted successfully"}

    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/")
def read_root():
    return {"message": "App is runing"}
