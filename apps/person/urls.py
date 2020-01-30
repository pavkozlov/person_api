from apps.person import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', views.PersonViewSet)
urlpatterns = router.urls
