"""API routers."""
from django.conf.urls import url
from rest_framework import routers

from api.auth import obtain_auth_token
from core import views as core_views
from profiles import views as profiles_views
from register import views as register_views
from users import views as users_views
from visits import views as visits_views
import projects.views
import dynamicforms.views

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
router.register('students', profiles_views.StudentViewSet, base_name='student')

# Register views
router.register('registrations', register_views.RegistrationViewSet)

# Visits views
router.register('visits', visits_views.VisitViewSet)
router.register('participations', visits_views.ParticipationsViewSet)
router.register('places', visits_views.PlaceViewSet)

# Projects views
router.register('projects', projects.views.ProjectViewSet)
router.register('project-participations', projects.views.ParticipationViewSet)
router.register('editions', projects.views.EditionViewSet)

# Dynamic forms views
router.register('forms', dynamicforms.views.FormViewSet)
router.register('form-entries', dynamicforms.views.FormEntryViewSet)

# Core views
router.register('documents', core_views.DocumentViewSet)


urlpatterns += router.urls
