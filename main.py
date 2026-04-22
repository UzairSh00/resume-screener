from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pdfplumber
import io
from database import engine, get_db
import models
import schemas
from screener import analyze_resume

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Resume Screener is running!"}

@app.get("/ui")
def serve_ui():
    return FileResponse("index.html")

@app.post("/screen", response_model=schemas.ScreeningResponse)
async def screen_resume(
    candidate_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    contents = await resume.read()
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        resume_text = ""
        for page in pdf.pages:
            resume_text += page.extract_text() or ""

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    result = analyze_resume(resume_text, job_description)

    screening = models.Screening(
        candidate_name=candidate_name,
        job_title=job_title,
        job_description=job_description,
        resume_text=resume_text,
        match_score=result["match_score"],
        missing_skills=result["missing_skills"],
        suggestions=result["suggestions"]
    )

    db.add(screening)
    db.commit()
    db.refresh(screening)

    return screening

@app.get("/history", response_model=list[schemas.ScreeningResponse])
def get_history(db: Session = Depends(get_db)):
    screenings = db.query(models.Screening).all()
    return screenings

@app.get("/history/{id}", response_model=schemas.ScreeningResponse)
def get_screening(id: int, db: Session = Depends(get_db)):
    screening = db.query(models.Screening).filter(models.Screening.id == id).first()
    if not screening:
        raise HTTPException(status_code=404, detail="Screening not found")
    return screening