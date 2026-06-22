from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.protocols.models import Protocol
from apps.protocols.serializers import ProtocolSerializer
from apps.protocols.services.workflow import (
    InvalidTransitionError,
    ProtocolWorkflowService,
)


class ProtocolViewSet(viewsets.ModelViewSet):

    queryset = Protocol.objects.all()

    serializer_class = ProtocolSerializer

    def _workflow_response(
        self,
        workflow_function,
        protocol,
        user,
    ):
        try:

            workflow_function(
                protocol=protocol,
                changed_by=user,
            )

            return Response(
                {
                    "status": protocol.status,
                }
            )

        except InvalidTransitionError as exc:

            return Response(
                {
                    "error": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=True,
        methods=["post"],
    )
    def submit(self, request, pk=None):

        protocol = self.get_object()

        return self._workflow_response(
            ProtocolWorkflowService.submit,
            protocol,
            request.user,
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def start_review(self, request, pk=None):

        protocol = self.get_object()

        return self._workflow_response(
            ProtocolWorkflowService.start_review,
            protocol,
            request.user,
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def approve(self, request, pk=None):

        protocol = self.get_object()

        return self._workflow_response(
            ProtocolWorkflowService.approve,
            protocol,
            request.user,
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def reject(self, request, pk=None):

        protocol = self.get_object()

        return self._workflow_response(
            ProtocolWorkflowService.reject,
            protocol,
            request.user,
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def request_revisions(self, request, pk=None):

        protocol = self.get_object()

        return self._workflow_response(
            ProtocolWorkflowService.request_revisions,
            protocol,
            request.user,
        )
