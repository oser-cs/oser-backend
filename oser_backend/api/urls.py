"""API routers."""
from django.conf.urls import url
from rest_framework import routers

from api.auth import obtain_auth_token
from core import views as core_views
from profiles import views as profiles_views
from register import views as register_views
from tutoring import views as tutoring_views
from users import views as users_views
from visits import views as visits_views

app_name = 'api'

# Register API routes here

urlpatterns = [
    url(r'^auth/get-token/$', obtain_auth_token, name='get-auth-token'),
]

router = routers.DefaultRouter(trailing_slash=True)

# Users views
router.register('users', users_views.UserViewSet)

# Profiles views
router.register('tutors', profiles_views.TutorViewSet)
router.register('students', profiles_views.StudentViewSet)

# Tutoring views
router.register('schools', tutoring_views.SchoolViewSet)
router.register('groups', tutoring_views.TutoringGroupViewSet,
                base_name='tutoring_group')
router.register('sessions', tutoring_views.TutoringSessionViewSet,
                base_name='tutoring_session')

# Register views
router.register('registrations', register_views.RegistrationViewSet)

# Visits views
router.register('visits', visits_views.VisitViewSet)
router.register('participants', visits_views.ParticipationsViewSet,
                base_name='participants')
router.register('places', visits_views.PlaceViewSet)

# Core views
router.register('documents', core_views.DocumentViewSet)

urlpatterns += router.urls
