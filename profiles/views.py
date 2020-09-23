"""Profile API views."""

from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from visits.serializers import VisitSerializer

from .models import Student, Tutor
from .serializers import StudentSerializer, TutorSerializer


User = get_user_model()


class TutorViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint that allows tutors to be viewed."""

    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = (DRYPermissions,)


class StudentViewSet(viewsets.ModelViewSet):
    """API endpoint that allows students to be viewed, and profiles to be updated."""

    def get_serializer(self, *args, **kwargs):
            kwargs['partial'] = True
            return super(StudentViewSet, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        else:
            return Student.objects.filter(user_id = user.id)

    serializer_class = StudentSerializer
    permission_classes = (DRYPermissions,)

    @action(detail=True)
    def visits(self, request, pk=None):
        """List detailed info about the visits a student participates in."""
        # NOTE: Only available for student users for now.
        user = User.objects.get(pk=pk)
        visits = user.visit_set.all()
        serializer = VisitSerializer(visits, many=True,
                                     context={'request': request})
        return Response(serializer.data)
