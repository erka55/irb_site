from .models import AuditLog


def log_event(
    *,
    action,
    entity_type,
    entity_id,
    actor=None,
    tenant=None,
    payload=None,
    event_id=None,
    occurred_at=None,
):
    return AuditLog.objects.create(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor=actor,
        tenant=tenant,
        payload=payload or {},
        event_id=event_id,
        occurred_at=occurred_at,
    )
