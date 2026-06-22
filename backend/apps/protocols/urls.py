from rest_framework.routers import DefaultRouter

from apps.protocols.views import ProtocolViewSet


router = DefaultRouter()

router.register(
    r"protocols",
    ProtocolViewSet,
    basename="protocols",
)

urlpatterns = router.urls
