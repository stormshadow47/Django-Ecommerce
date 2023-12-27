import logging
from Users.backends import UserProfileAuthBackend
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import ValidationError
from rest_framework import status, generics
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from Users.models import UserProfile
from Users.serializers import UserProfileSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Send Welcome Email
        send_mail(
            'Welcome to Our Platform',
            'Thank you for registering!',
            'nithin.raj101@outlook.com',  # Replace with your email sender
            [email],  # Email address of the user
            fail_silently=False,
        )
        
        # Create UserProfile (or any additional profile data)
        profile = UserProfile.objects.create(user=user)
        
        return Response({'message': 'Registration successful. Welcome email sent.'}, status=201)
    
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def logout(request):
    refresh_token = request.data.get('refresh_token')

    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=400)
    
    # Generate the reset token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Construct reset link
    reset_url = f'http://localhost:8000/reset/{uid}/{token}/'  # Using localhost as a placeholder
    
    # Compose the email content
    subject = 'Password Reset Request'
    message = f'Please use the following link to reset your password: {reset_url}'
    from_email = 'nithin.raj101@outlook.com'  # Replace with your email address
    
    # Send the email
    send_mail(subject, message, from_email, [email])
    
    return JsonResponse({'message': 'Password reset email sent successfully'}, status=200)


logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError) as e:
        logger.exception(f"Password reset confirm error: {e}")
        user = None
    
    if user and default_token_generator.check_token(user, token):
        return JsonResponse({'message': 'Valid token. Proceed to set a new password'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    


@api_view(['POST'])
@permission_classes([AllowAny])
def set_new_password(request, uidb64, token):
    new_password = request.data.get('new_password')
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError) as e:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    if user and default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return JsonResponse({'message': 'Password updated successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def admin_logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class user_list(generics.ListAPIView):
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    #permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class user_detail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    #permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@api_view(['POST'])
#@permission_classes([IsAdminUser])
@authentication_classes([UserProfileAuthBackend, SessionAuthentication])
def send_custom_email(request):
    subject = request.data.get('subject')
    html_message = request.data.get('html_message')
    recipient_list_str = request.data.get('recipient_list', '')  # String of recipients

    if subject and html_message and recipient_list_str:
        recipient_list = recipient_list_str.split(',')  # Convert string to list of recipients

        # Generate a plain text version from HTML
        plain_text_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_text_message,
            'nithin.raj101@outlook.com',  # Replace with your sender email
            recipient_list,
            html_message=html_message,
        )
        return Response({'success': 'Email sent successfully'})
    else:
        return Response({'error': 'Please provide subject, html_message, and recipient_list'}, status=400)