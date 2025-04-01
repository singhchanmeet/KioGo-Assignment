from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User, AllowedDomains
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .authentication import CustomJWTAuthentication

def generate_otp():
    import random
    import string
    otp = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return otp

# Create your views here.

from api.permissions import IsAuthenticated  # Import your custom permission

class UserDetails(APIView):
    # Use custom permission class
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Authentication and permission will be handled by CustomJWTAuthentication 
        # and IsAuthenticated class
        
        # Get user data using your existing serializer
        try:
            user = request.user
            serializer_data = UserSerializer(user).data
            
            # Remove sensitive fields
            if 'one_time_password' in serializer_data:
                serializer_data.pop('one_time_password')
                
            return Response(serializer_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserRegister(APIView):

    def post(self, request):
        # Extract email from request data
        email = request.data.get('email')
        
        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if domain is allowed
        domain = email.split('@')[1]
        if domain not in AllowedDomains.objects.values_list('domain', flat=True):
            return Response({'message': 'Domain Not Allowed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate OTP
        otp = generate_otp()
        
        # Check if user already exists
        user_exists = User.objects.filter(email=email).exists()
        
        if user_exists:
            # Update existing user's OTP
            user = User.objects.get(email=email)
            user.one_time_password = otp
            user.pasword_expiry_time = timezone.now() + datetime.timedelta(minutes=5)
            user.save()
        else:
            # Create new user
            user_data = {
                'email': email,
                'one_time_password': otp,
                'pasword_expiry_time': timezone.now() + datetime.timedelta(minutes=5)
            }
            user_serializer = UserSerializer(data=user_data)
            
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Send OTP email
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        subject = 'One Time Password'
        message = f'Your One Time Password is: {otp}'
        
        send_mail(subject, message, email_from, recipient_list)
        
        # Return successful response
        return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)
    
import jwt
import datetime


class TokenObtainView(APIView):
    """
    Custom token endpoint that verifies the one-time password (OTP)
    and provides manually generated JWT tokens.
    """
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('one_time_password')
        
        if not email or not otp:
            return Response(
                {'message': 'Email and verification code are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Find the user by email
            user = User.objects.get(email=email)
            
            # Check if OTP matches and is not expired
            current_time = timezone.now()
            
            if user.one_time_password != otp:
                return Response(
                    {'message': 'Invalid verification code'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if current_time > user.pasword_expiry_time:
                return Response(
                    {'message': 'Verification code has expired'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Manually generate JWT tokens instead of using RefreshToken.for_user
            # Create access token payload
            access_payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
                'token_type': 'access'
            }
            
            # Create refresh token payload
            refresh_payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'token_type': 'refresh'
            }
            
            # Generate tokens
            access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
            refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
            
            # Return the token pair
            return Response({
                'refresh': refresh_token,
                'access': access_token,
            })
            
        except User.DoesNotExist:
            return Response(
                {'message': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
            
# Add this to your api/views.py file

class TokenRefreshView(APIView):
    """
    Custom token refresh endpoint that takes a refresh token and returns a new access token.
    """
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'message': 'Refresh token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Decode the refresh token
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Check that it's actually a refresh token
            token_type = payload.get('token_type')
            if token_type != 'refresh':
                return Response(
                    {'message': 'Invalid token type'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Get user from the token
            user_id = payload.get('user_id')
            if not user_id:
                return Response(
                    {'message': 'Invalid token payload'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Get the user from database
            user = User.objects.get(id=user_id)
            
            # Generate a new access token
            access_payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
                'token_type': 'access'
            }
            
            access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
            
            return Response({
                'access': access_token,
            })
        except jwt.ExpiredSignatureError:
            return Response(
                {'message': 'Refresh token has expired'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return Response(
                {'message': 'Invalid refresh token'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except User.DoesNotExist:
            return Response(
                {'message': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'message': f'An error occurred: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )