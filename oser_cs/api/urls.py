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
router.register(r'schools', tutoring.SchoolViewSet)
router.register(r'tutoring/groups', tutoring.TutoringGroupViewSet,
                base_name='tutoring_group')
router.register(r'tutoring/sessions', tutoring.TutoringSessionViewSet,
                base_name='tutoring_session')

urlpatterns += router.urls
