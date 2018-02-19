"""API routers."""
from rest_framework import routers

from users import views as users_views
from tutoring import views as tutoring_views
from showcase_site import views as showcase_site_views

app_name = 'api'

# Register API routes here

router = routers.DefaultRouter()

# Users views
router.register(r'users', users_views.UserViewSet)
router.register(r'tutors', users_views.TutorViewSet)
router.register(r'students', users_views.StudentViewSet)
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

urlpatterns = router.urls
