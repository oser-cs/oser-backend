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

# users
router.register(r'users', users.UserViewSet)

# persons
router.register(r'tutors', persons.TutorViewSet)
router.register(r'students', persons.StudentViewSet)
router.register(r'schoolstaffmembers', persons.SchoolStaffMemberViewSet)

# tutoring
router.register(r'tutoringgroups', tutoring.TutoringGroupViewSet)
router.register(r'schools', tutoring.SchoolViewSet)

urlpatterns += router.urls
