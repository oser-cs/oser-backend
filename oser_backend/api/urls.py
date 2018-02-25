"""API routers."""
from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from api.auth import obtain_auth_token
from showcase_site import views as showcase_site_views
from tutoring import views as tutoring_views
from users import views as users_views
from visits import views as visits_views

app_name = 'api'

# Register API routes here

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    url(r'^auth/get-token/$', obtain_auth_token, name='get-auth-token'),
]

router = routers.SimpleRouter()

# Visits views
router.register('visits', visits_views.VisitViewSet)
router.register('visit-participants', visits_views.VisitParticipantsViewSet,
                base_name='visit-participants')

# Users views
router.register(r'users', users_views.UserViewSet)
router.register(r'tutors', users_views.TutorViewSet)
router.register(r'students', users_views.StudentViewSet)
# router.register('student-visits', users_views.StudentVisitsViewSet)
router.register(r'schoolstaffmembers', users_views.SchoolStaffMemberViewSet)

# Tutoring views
router.register(r'schools', tutoring_views.SchoolViewSet)
router.register(r'tutoring/groups', tutoring_views.TutoringGroupViewSet,
                base_name='tutoring_group')
router.register(r'tutoring/sessions', tutoring_views.TutoringSessionViewSet,
                base_name='tutoring_session')

# Showcase site views
router.register(r'articles', showcase_site_views.ArticleViewSet)
router.register(r'categories', showcase_site_views.CategoryViewSet)
router.register(r'testimonies', showcase_site_views.TestimonyViewSet)
router.register(r'keyfigures', showcase_site_views.KeyFigureViewSet)

urlpatterns += router.urls
