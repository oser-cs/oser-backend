"""API authentication."""

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.serializers import UserSerializer


class ObtainAuthTokenUser(ObtainAuthToken):
    """Custom obtain_auth_token view to return token AND user."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user, context={'request': request})
        return Response({'token': token.key, 'user': user_serializer.data})


obtain_auth_token = ObtainAuthTokenUser.as_view()
