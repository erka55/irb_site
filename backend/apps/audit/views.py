from rest_framework import viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from apps.audit.access import AuditLogAccessService
from apps.audit.models import AuditLog
from apps.audit.serializers import (
    AuditLogFilterSerializer,
    AuditLogSerializer,
)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AuditLogSerializer

    def get_queryset(self):
        tenant_id = self._get_tenant_id()

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

        filter_serializer = AuditLogFilterSerializer(
            data=request.query_params,
        )

        filter_serializer.is_valid(
            raise_exception=True,
        )

        filters = filter_serializer.validated_data

        queryset = AuditLogAccessService.list_logs(
            user_id=request.user.id,
            tenant_id=tenant_id,
            actor_id=filters.get(
                "actor_id",
            ),
            action=filters.get(
                "action",
            ),
            entity_type=filters.get(
                "entity_type",
            ),
            entity_id=filters.get(
                "entity_id",
            ),
            event_id=filters.get(
                "event_id",
            ),
            occurred_from=filters.get(
                "occurred_from",
            ),
            occurred_to=filters.get(
                "occurred_to",
            ),
        )

        page = self.paginate_queryset(
            queryset,
        )

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

        return Response(
            serializer.data,
        )

    def retrieve(
        self,
        request,
        *args,
        **kwargs,
    ):
        self._check_access()

        instance = self.get_queryset().filter(
            pk=kwargs["pk"],
        ).first()

        if instance is None:
            raise NotFound(
                "Audit log not found."
            )

        serializer = self.get_serializer(
            instance,
        )

        return Response(
            serializer.data,
        )
