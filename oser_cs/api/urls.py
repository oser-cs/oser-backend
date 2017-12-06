"""API routers."""
from django.urls import path, include

from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from . import views

API_TITLE = 'oser-cs.fr - API'

app_name = 'api'

urlpatterns = [
    path('docs/', get_swagger_view(title=API_TITLE)),
    path('schema/', get_schema_view(title=API_TITLE)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework'))
]

# Create your routes here

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('tutors', views.TutorViewSet)
router.register('tutoringgroups', views.TutoringGroupViewSet)

urlpatterns += router.urls
