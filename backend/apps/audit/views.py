from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.audit.access import AuditLogAccessService
from apps.audit.models import AuditLog
from apps.audit.serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AuditLogSerializer

    def get_queryset(self):
        tenant_id = getattr(
            self.request,
            "tenant_id",
            None,
        )

        if tenant_id is None:
            return AuditLog.objects.none()

        return AuditLog.objects.filter(
            tenant_id=tenant_id,
        )

    def _get_tenant_id(self):
        tenant_id = getattr(
            self.request,
            "tenant_id",
            None,
        )

        if tenant_id is None:
            raise PermissionDenied(
                "Tenant context is required."
            )

        return tenant_id

    def _check_access(self):
        tenant_id = self._get_tenant_id()

        user = self.request.user

        if not user or not user.is_authenticated:
            raise PermissionDenied(
                "Authentication is required."
            )

        if not AuditLogAccessService.can_view(
            user_id=user.id,
            tenant_id=tenant_id,
        ):
            raise PermissionDenied(
                "User does not have permission to view audit logs."
            )

        return tenant_id

    def list(self, request, *args, **kwargs):
        tenant_id = self._check_access()

        queryset = AuditLog.objects.filter(
            tenant_id=tenant_id,
        )

        queryset = self._apply_filters(
            queryset,
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
            )
            return self.get_paginated_response(
                serializer.data,
            )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        tenant_id = self._check_access()

        instance = AuditLog.objects.filter(
            tenant_id=tenant_id,
            pk=kwargs["pk"],
        ).first()

        if instance is None:
            from rest_framework.exceptions import NotFound

            raise NotFound(
                "Audit log not found."
            )

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def _apply_filters(self, queryset):
        action = self.request.query_params.get(
            "action",
        )

        entity_type = self.request.query_params.get(
            "entity_type",
        )

        entity_id = self.request.query_params.get(
            "entity_id",
        )

        event_id = self.request.query_params.get(
            "event_id",
        )

        actor_id = self.request.query_params.get(
            "actor_id",
        )

        if action:
            queryset = queryset.filter(
                action=action,
            )

        if entity_type:
            queryset = queryset.filter(
                entity_type=entity_type,
            )

        if entity_id:
            queryset = queryset.filter(
                entity_id=entity_id,
            )

        if event_id:
            queryset = queryset.filter(
                event_id=event_id,
            )

        if actor_id:
            queryset = queryset.filter(
                actor_id=actor_id,
            )

        return queryset
