from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .renderers import TokenRenderer
from django.contrib.auth import get_user_model
User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    pass
    # renderer_classes = (TokenRenderer,)


class MyTokenRefreshView(TokenRefreshView):
    pass
    # renderer_classes = (TokenRenderer,)


class UserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListUsersView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            users = User.objects.filter(is_staff=False)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Something went wrong when trying to load users'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
