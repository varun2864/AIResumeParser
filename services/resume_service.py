#business logic (receives resume, extracts skill names, and stores them in database)

from sqlalchemy.orm import Session
from models import Resume


def create_resume(
    *, #ensures that all parameters are keyword arguments
    session: Session,
    candidate_name: str,
    resume_url: str,
) -> Resume:
    existing = ( #checks for preexisting resume
        session.query(Resume)
        .filter(Resume.resume_url == resume_url)
        .one_or_none()
    )

    if existing:
        return existing

    resume = Resume(
        candidate_name=candidate_name,
        resume_url=resume_url,
    )

    session.add(resume)
    session.flush() #pushes data to database
    session.refresh(resume) #updates object with database data

    return resume
