from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import CustomUser as User
from utils.helpers import send_thankyou_email

class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer = RegistrationSerializer

    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self,request,*args,**kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user == None:
            return Response({"error":"email was not sent"},status=401)

        return Response({"detial":"otp has being sent to you email"},status=201)

class PasswordResetView(APIView):
    permission_classes = (AllowAny,)
    serializer =  PasswordResetSerializer

    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self,request,*args,**kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_eamil = serializer._action_send()
        if not send_eamil:
            return Response({"error":"email was not sent"},status=401)

        return Response({"detial":"otp has being sent to you email"},status=200)
    
class VerifyOtpView(APIView):
    permission_classes = (AllowAny,)
    serializers = VerifyOtpSerializer

    @swagger_auto_schema(request_body=VerifyOtpSerializer)
    def post(self,request):
        serializer = self.serializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        
        send_thankyou_email(
            email=email,
            username=user.username,
        )

        return Response({"detial":"account is active now"},status=200)
    

class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)
    serializers = VerifyOtpSerializer

    @swagger_auto_schema(request_body=VerifyOtpSerializer)
    def post(self,request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"detial":""},status=200)
    
class ResendEmailView(PasswordResetView):
    permission_classes = (AllowAny,)
    serializers = VerifyOtpSerializer