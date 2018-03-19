"""API routers."""
from django.conf.urls import url
from rest_framework import routers

from api.auth import obtain_auth_token
from showcase_site import views as showcase_site_views
from tutoring import views as tutoring_views
from users import views as users_views
from visits import views as visits_views

app_name = 'api'

# Register API routes here

urlpatterns = [
    url(r'^auth/get-token/$', obtain_auth_token, name='get-auth-token'),
]

router = routers.DefaultRouter(trailing_slash=True)

# Visits views
router.register('visits', visits_views.VisitViewSet)
router.register('visit-participants', visits_views.VisitParticipantsViewSet,
                base_name='visit-participants')
router.register('places', visits_views.PlaceViewSet)

# Users views
router.register('users', users_views.UserViewSet)
router.register('tutors', users_views.TutorViewSet)
router.register('students', users_views.StudentViewSet)
# router.register('student-visits', users_views.StudentVisitsViewSet)
router.register('schoolstaffmembers', users_views.SchoolStaffMemberViewSet)

# Tutoring views
router.register('schools', tutoring_views.SchoolViewSet)
router.register('tutoring/groups', tutoring_views.TutoringGroupViewSet,
                base_name='tutoring_group')
router.register('tutoring/sessions', tutoring_views.TutoringSessionViewSet,
                base_name='tutoring_session')

# Showcase site views
router.register('articles', showcase_site_views.ArticleViewSet)
router.register('categories', showcase_site_views.CategoryViewSet)
router.register('testimonies', showcase_site_views.TestimonyViewSet)
router.register('keyfigures', showcase_site_views.KeyFigureViewSet)
router.register('partners', showcase_site_views.PartnerViewSet)

urlpatterns += router.urls
