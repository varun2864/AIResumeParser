from database import SessionLocal

from services.pdf_service import extract_text_from_pdf
from services.skill_service import extract_skills

from models import Resume, Skill


def process_resume(resume_id: int, file_bytes: bytes):

    print("resume processing started for resume ID: ", resume_id)
    session = SessionLocal()

    try:
        resume = (session.query(Resume).filter(Resume.id == resume_id).one_or_none())

        if resume is None:
            return
        
        text = extract_text_from_pdf(file_bytes)
        print(f"Extracted text length: {len(text)}")
        
        skills = extract_skills(text)
    
        for skill_name in skills: #checks if skill already exists in db
            skill = (session.query(Skill).filter(Skill.name == skill_name).one_or_none())

            if skill is None: #if new skill, append to db
                skill = Skill(name=skill_name)
                session.add(skill)

            resume.skills.append(skill)

        session.commit()
    
    except Exception:
        session.rollback()
        raise
    
    finally:
        session.close()
    


