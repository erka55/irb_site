from apps.meetings.models import Meeting, MeetingAgenda
from apps.protocols.models import Protocol


class AgendaService:

    @staticmethod
    def add_protocol(
        meeting: Meeting,
        protocol: Protocol,
        order: int,
        presenter=None,
        notes="",
    ):
        return MeetingAgenda.objects.create(
            meeting=meeting,
            protocol=protocol,
            order=order,
            presenter=presenter,
            notes=notes,
        )

    @staticmethod
    def remove_agenda_item(agenda: MeetingAgenda):
        agenda.delete()

    @staticmethod
    def reorder_agenda(
        agenda: MeetingAgenda,
        new_order: int,
    ):
        agenda.order = new_order
        agenda.save(update_fields=["order"])

        return agenda
