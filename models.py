from sqlalchemy import Column, Integer, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

resume_skills = Table(
    "resume_skills",
    Base.metadata,
    Column(
        "resume_id",
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "skill_id",
        ForeignKey("skills.id"),
        primary_key=True,
    ),
)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True)
    candidate_name = Column("name", Text, nullable=False)
    resume_url = Column(Text, nullable=False, unique = True) #ensures no duplicate r    esumes

    skills = relationship(
        "Skill",
        secondary=resume_skills,
        back_populates="resumes",
    )


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    resumes = relationship(
        "Resume",
        secondary=resume_skills,
        back_populates="skills",
    )
