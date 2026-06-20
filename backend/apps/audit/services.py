from .models import AuditLog

def log_event(
    *,
    action,
    entity_type,
    entity_id,
    actor=None,
    tenant=None,
    payload=None,
):
    return AuditLog.objects.create(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor=actor,
        tenant=tenant,
        payload=payload or {},
    )
