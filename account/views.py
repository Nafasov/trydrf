from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    Token.objects.filter(user=user).delete()
    data = {
        'success': True,
        'message': 'Logged out successfully'
    }
    return Response(data, status=status.HTTP_200_OK)

