from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.staticfiles import StaticFiles

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from pydantic import BaseModel

from models import Resume, Skill
from database import get_session

from services.resume_service import create_resume
from services.storage_service import upload_resume
from services.background_tasks import process_resume

class ResumeResponse(BaseModel):
    id: int
    candidate_name: str
    skills: list[str]


app = FastAPI()

app.mount( #mounts static files (makes locally stored files accessible via URL)
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

@app.post("/resumes", response_model=ResumeResponse) #POST route
def create_resume_endpoint(
    candidate_name: str,
    background_tasks: BackgroundTasks,
    f: UploadFile = File(...), #ensures file is uploaded
    session : Session = Depends(get_session) #ensures session is created before function is called
):
    try:
        file_bytes = f.file.read() #converts file to bytes

        resume_url = upload_resume(
            file_bytes = file_bytes, #passes file bytes
            filename = f.filename) #passes file name
        
        resume = create_resume(
            session = session, 
            candidate_name = candidate_name,
            resume_url = resume_url,

        )
        
        session.commit() #ensures transaction is committed so background task can find it

        background_tasks.add_task( #schedules func to run after response    
            process_resume, #function to be ran in background
            resume_id = resume.id, #parameters passed to function
            file_bytes = file_bytes
        )
    
        return ResumeResponse(
            id=resume.id,
            candidate_name=resume.candidate_name,
            skills=[]
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code = 409, 
            detail = "constraint violation while creating resume")

@app.get("/resumes/search", response_model=list[ResumeResponse])
def search_resumes(
    skills: list[str] = Query(...), #ensures skills are query parameters, not request body
    session: Session = Depends(get_session)
):
    
    skill_names = [skill.strip().lower() for skill in skills]

    resumes = (
        session.query(Resume)
        .join(Resume.skills)
        .filter(Skill.name.in_(skill_names))
        .group_by(Resume.id) #grouping by resume id
        .having(func.count(Resume.id) == len(skill_names)) #must match all requested skills
        .all()
    )

    return [ResumeResponse(
        id = resume.id,
        candidate_name = resume.candidate_name,
        skills = [skill.name for skill in resume.skills]
    ) for resume in resumes]


@app.get("/resumes/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int, 
    session: Session = Depends(get_session)
):
    resume = session.query(Resume).filter(Resume.id == resume_id).one_or_none()
    
    if resume is None:
        raise HTTPException(
            status_code = 404,
            detail = "resume not found")
        
    return ResumeResponse(
        id = resume_id,
        candidate_name = resume.candidate_name,
        skills = []
    )




