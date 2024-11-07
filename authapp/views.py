from rest_framework.views import APIView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .serializers import CustomUserSerializer, JWTSerializer, UserChangePasswordSerializer, UserPasswordResetSerializer, SendPasswordResetEmailSerializer
from rest_framework.permissions import IsAuthenticated
from .forms import *

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = JWTSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create a serializer instance with cleaned form data
            serializer = CustomUserSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                user = serializer.save()  # Save the user

                # Generate email verification token
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verification_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
                activate_url = f"http://{current_site.domain}{verification_link}"
                
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'activate_url': activate_url,
                })
                send_mail(
                    mail_subject,
                    message,
                    'godhanidaksh016@gmail.com',  # From email
                    [user.email],  # To email
                    fail_silently=False,
                )
                
                return render(request, 'check_email.html')  # Redirect to login on successful signup
            else:   
                # Add API serializer errors to the form
                for field, errors in serializer.errors.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'activation_invalid.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Initialize JWTSerializer with form data for validation
            serializer = JWTSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                # Process the validated data as needed, such as storing the token
                # Here you could add the token to the session or cookies if needed
                return redirect('home')  # Redirect to home on successful login
            else:
                # Add serializer errors to the form
                for field, errors in serializer.errors.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def home_view(request):
    context = {}  # You can add context data here if needed
    return render(request, 'home.html', context)

class UserChangePasswordView(APIView):
  
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
  
class SendPasswordResetEmailView(APIView):
  
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
  
class UserPasswordResetView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)