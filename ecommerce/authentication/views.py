from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token  
from .serializers import UserSerializer
from .models import User
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s')

class SignupView(APIView):
    '''AllowAny is a permission class in rest_framework.permissions'''
    permission_classes = [AllowAny]

    def post(self, request):
        ''' POST request for sign up the user. '''
        logging.info(f'request.data: {request.data}')
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # create token for the user
            token, _ = Token.objects.get_or_create(user=user) 
            return Response({'token': token.key, 'user': serializer.data})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    ''' POST request for login the user'''
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            logging.info(f'user: {user}')
            if user.check_password(request.data['password']):
                logging.info(f'check_password success')
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_type': user.user_type})
            return Response({'error': 'Invalid credentials'}, status=401)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=401)