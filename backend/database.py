# Import necessary libraries
import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define database connection using Azure SQL Database
DATABASE_URL = os.getenv("DATABASE_URL", "mssql+pyodbc://USERNAME:PASSWORD@SERVER_NAME.database.windows.net/DATABASE_NAME?driver=ODBC+Driver+17+for+SQL+Server")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Transcription model
class Transcription(Base):
    __tablename__ = "transcriptions"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    transcript = Column(String)
    speakers = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)
