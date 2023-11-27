from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from apps.account.serializers import RegisterSerializer, UserSerializer
from rest_framework.generics import ListAPIView, GenericAPIView
from django.contrib.auth import get_user_model
from .send_mail import send_confirmation_email
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from config.tasks import  send_activation_sms_task, send_confirmation_email_task
from .send_sms import send_activation_sms

User = get_user_model()

class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                # send_confirmation_email(user.email, user.activation_code)
                send_confirmation_email_task.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but troubleswith email', 'data': serializer.data}, status=201)
        return Response(serializer.data, status=201)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Succesfuly activated', status=200)


# 02defedf-9263-48c3-8219-308a0691211c


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )


class RegistrationPhoneView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # send_activation_sms(user.phone_number, user.activation_code)
            send_activation_sms_task.delay(user.phone_number, user.activation_code)
            return Response('Succesfully registered', status=201)


class ActivationPhoneView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = User.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Succesfuly activated', status=200)
