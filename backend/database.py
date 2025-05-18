# Import necessary libraries
import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define database connection
# Use SQLite for development/local testing if Azure SQL connection is not available
DATABASE_URL = os.getenv("AZURE_SQL_CONNECTION_STRING")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./transcriptions.db"
    print("Warning: Using SQLite database for development. Configure AZURE_SQL_CONNECTION_STRING for production.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Recording model
class Recording(Base):
    __tablename__ = "recordings"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    audio_data = Column(LargeBinary)  # Store audio file
    transcript = Column(Text)
    language = Column(String, default="en")
    speakers = Column(Text)  # JSON string with speaker information
    duration = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'transcript': self.transcript,
            'language': self.language,
            'speakers': self.speakers,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Create database tables
Base.metadata.create_all(bind=engine)