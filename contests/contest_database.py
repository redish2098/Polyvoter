from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, create_engine, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import os
from pathlib import Path
from flask import g
from contextlib import contextmanager

Base = declarative_base()

DB_FILE = Path(__file__).resolve().parent / "submissions" / "contests.db"

class Contests(Base):
    __tablename__ = 'contests'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    date = Column(Date)

    submissions = relationship('Submissions', back_populates='contest')

class Submissions(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    contest_id = Column(Integer, ForeignKey('contests.id'))
    author = Column(String)
    text = Column(String)
    avg = Column(Float)
    sum = Column(Integer)
    count = Column(Integer)

    contest = relationship('Contests', back_populates='submissions')
    attachments = relationship('Attachments', back_populates='submission')

class Attachments(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submissions.id'))
    filename = Column(String)

    submission = relationship('Submissions', back_populates='attachments')
    variants = relationship('AttachmentVariants', back_populates='attachment', cascade='all, delete-orphan')

    def get_variant(self, kind):
        return next((v for v in self.variants if v.kind == kind), None)

class AttachmentVariants(Base):
    __tablename__ = 'attachment_variants'
    id = Column(Integer, primary_key=True)
    attachment_id = Column(Integer, ForeignKey('attachments.id'))
    kind = Column(String)
    filename = Column(String)

    attachment = relationship('Attachments', back_populates='variants')

    __table_args__ = (UniqueConstraint('attachment_id', 'kind', name='uq_attachment_variant_kind'),)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_app(app):
    @app.teardown_appcontext
    def close_session(exception=None):
        session = g.pop('db_session', None)
        if session is not None:
            if exception is None:
                session.commit()
            else:
                session.rollback()
            session.close()

os.makedirs(DB_FILE.parent, exist_ok=True)
engine = create_engine(f"sqlite:///{DB_FILE}")
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)