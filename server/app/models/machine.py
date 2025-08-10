from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Machine(Base):
    __tablename__ = "machines"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, unique=True, index=True, nullable=False)  # e.g., UUID from utility
    hostname = Column(String, nullable=True)
    os_name = Column(String, nullable=True)
    os_version = Column(String, nullable=True)
    last_checkin = Column(DateTime, default=datetime.utcnow)
    machine_metadata = Column("metadata", JSON, nullable=True)

    # relationship to check results (one-to-many)
    checks = relationship("CheckResult", back_populates="machine", cascade="all, delete-orphan")


class CheckResult(Base):
    __tablename__ = "check_results"
    id = Column(Integer, primary_key=True, index=True)
    machine_id_fk = Column(Integer, ForeignKey("machines.id"), nullable=False)
    check_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # e.g., "ok", "warning", "fail"
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    machine = relationship("Machine", back_populates="checks")
