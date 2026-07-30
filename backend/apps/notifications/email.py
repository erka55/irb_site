import logging

logger = logging.getLogger(__name__)


class EmailBackend:
    """
    Email backend stub.
    """

    @staticmethod
    def send(subject, message, recipient):
        logger.info(
            "Email sent to %s (%s)",
            recipient,
            subject,
        )

        return True
