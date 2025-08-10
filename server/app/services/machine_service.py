from sqlalchemy.orm import Session
import models
from schemas.machine import CheckInPayload
from datetime import datetime


def upsert_machine_and_checks(db: Session, payload: CheckInPayload):
    # Get existing machine
    machine = db.query(models.machine.Machine).filter(models.machine.Machine.machine_id == payload.machine_id).first()
    if not machine:
        machine = models.machine.Machine(
            machine_id=payload.machine_id,
            hostname=payload.hostname,
            os_name=payload.os_name,
            os_version=payload.os_version,
            metadata=payload.metadata or {},
            last_checkin=datetime.utcnow()
        )
        db.add(machine)
        db.flush()  # get id for foreign keys
    else:
        machine.hostname = payload.hostname or machine.hostname
        machine.os_name = payload.os_name or machine.os_name
        machine.os_version = payload.os_version or machine.os_version
        machine.metadata = payload.metadata or machine.metadata
        machine.last_checkin = datetime.utcnow()

    # Only create check results for provided checks (we store history)
    new_checks = []
    for ch in payload.checks or []:
        cr = models.machine.CheckResult(
            machine=machine,
            check_name=ch.name,
            status=ch.status,
            details=ch.details or {}
        )
        db.add(cr)
        new_checks.append(cr)

    db.commit()
    db.refresh(machine)
    return machine


import json

def list_machines(db: Session, os_name: str | None = None, status: str | None = None, limit: int = 100, offset: int = 0):
    q = db.query(models.machine.Machine)

    # Step 2: Optional OS filter
    if os_name:
        q = q.filter(models.machine.Machine.os_name == os_name)

    # Step 3: Optional status filter (latest check per machine)
    if status:
        from sqlalchemy import func
        sub = (
            db.query(
                models.machine.CheckResult.machine_id_fk,
                func.max(models.machine.CheckResult.created_at).label("m")
            )
            .group_by(models.machine.CheckResult.machine_id_fk)
            .subquery()
        )
        q = (
            q.join(
                models.machine.CheckResult,
                models.machine.Machine.id == models.machine.CheckResult.machine_id_fk
            )
            .join(
                sub,
                (models.machine.CheckResult.machine_id_fk == sub.c.machine_id_fk) &
                (models.machine.CheckResult.created_at == sub.c.m)
            )
            .filter(models.machine.CheckResult.status == status)
        )

    # Step 4: Apply ordering & pagination
    q = q.order_by(models.machine.Machine.last_checkin.desc()).limit(limit).offset(offset)

    # Step 5: Fetch data
    machines = q.all()

    # Step 6: Transform metadata into a dict
    result = []
    for m in machines:
        md = getattr(m, "metadata", None)
        if isinstance(md, str):
            import json
            try:
                md = json.loads(md)
            except json.JSONDecodeError:
                md = None
        elif not isinstance(md, dict):
            md = None

        result.append({
            "id": m.id,
            "machine_id": m.machine_id,
            "hostname": m.hostname,
            "os_name": m.os_name,
            "os_version": m.os_version,
            "last_checkin": m.last_checkin,
            "metadata": md,
            "checks": m.checks,
        })

    return result


def get_machine(db: Session, machine_id: int):
    machine = db.query(models.machine.Machine).filter(models.machine.Machine.id == machine_id).first()
    if machine and isinstance(machine.metadata, str):
        try:
            import json
            machine.metadata = json.loads(machine.metadata)
        except json.JSONDecodeError:
            machine.metadata = {}
    return machine

