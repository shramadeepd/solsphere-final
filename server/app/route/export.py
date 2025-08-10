from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from database import SessionLocal
import csv
from io import StringIO
from models import machine as machine_models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    # produce CSV with machines and their latest check
    from sqlalchemy import func
    sub = (
        db.query(machine_models.CheckResult.machine_id_fk, func.max(machine_models.CheckResult.created_at).label("m"))
        .group_by(machine_models.CheckResult.machine_id_fk)
        .subquery()
    )
    q = db.query(
        machine_models.Machine.machine_id,
        machine_models.Machine.hostname,
        machine_models.Machine.os_name,
        machine_models.Machine.os_version,
        machine_models.Machine.last_checkin,
        machine_models.CheckResult.check_name,
        machine_models.CheckResult.status,
    ).outerjoin(machine_models.CheckResult, machine_models.Machine.id == machine_models.CheckResult.machine_id_fk)\
     .outerjoin(sub, (machine_models.CheckResult.machine_id_fk == sub.c.machine_id_fk) & (machine_models.CheckResult.created_at == sub.c.m))

    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(["machine_id", "hostname", "os_name", "os_version", "last_checkin", "latest_check", "latest_status"])
    for row in q.all():
        writer.writerow([
            row.machine_id,
            row.hostname or "",
            row.os_name or "",
            row.os_version or "",
            row.last_checkin.isoformat() if row.last_checkin else "",
            row.check_name or "",
            row.status or ""
        ])
    return Response(content=buf.getvalue(), media_type="text/csv")
