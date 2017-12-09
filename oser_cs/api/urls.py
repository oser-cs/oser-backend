"""API routers."""
from django.urls import path, include
from rest_framework import routers

from .views import users, persons, tutoring

app_name = 'api'

urlpatterns = [
    path('api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
]

# Create your routes here

router = routers.DefaultRouter()
router.register(r'users', users.UserViewSet)
router.register(r'tutors', persons.TutorViewSet)
router.register(r'tutoringgroups', tutoring.TutoringGroupViewSet)

urlpatterns += router.urls
