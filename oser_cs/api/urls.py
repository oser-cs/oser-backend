"""API routers."""
from rest_framework import routers

from .views import users, tutoring

app_name = 'api'

urlpatterns = []

# Create your routes here

router = routers.DefaultRouter()

# users
router.register(r'users', users.UserViewSet)
router.register(r'tutors', users.TutorViewSet)
router.register(r'students', users.StudentViewSet)
router.register(r'schoolstaffmembers', users.SchoolStaffMemberViewSet)

# tutoring
router.register(r'schools', tutoring.SchoolViewSet)
router.register(r'tutoring/groups', tutoring.TutoringGroupViewSet,
                base_name='tutoring_group')
router.register(r'tutoring/sessions', tutoring.TutoringSessionViewSet,
                base_name='tutoring_session')

urlpatterns += router.urls
