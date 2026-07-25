from .base import BaseEvent


class ProtocolSubmitted(BaseEvent):
    pass


class ProtocolApproved(BaseEvent):
    pass


class ProtocolRejected(BaseEvent):
    pass


class ProtocolRevisionsRequested(BaseEvent):
    pass
