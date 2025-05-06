from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser as User
from utils.helpers import send_email_verification, generate_otp, send_password_reset, verify_otp

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
            "telephone",
            "password",
            "password2",
        ]

    
    # Validate Email
    def validate_email(self,value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exissts")
        return value
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exissts")
        return value

    def validate(self, attrs):
        password1= attrs.get("password")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise ValidationError(detail="password does not match")

        return super().validate(attrs)
    
    def save(self, **kwargs):
        print(self.validated_data)
        totp, secret_code = generate_otp()
        totp = totp.now()
        # send otp to user
        email_sent = send_email_verification(
            username=self.validated_data.get("username"),
            email=self.validated_data.get("email"),
            otp_code=totp,
        )

        user= None

        if email_sent:
            user = User.objects.create_user(
                first_name = self.validated_data.get("first_name"),
                middle_name = self.validated_data.get("middle_name"),
                last_name = self.validated_data.get("last_name"),
                username = self.validated_data.get("username"),
                email = self.validated_data.get("email"),
                telephone = self.validated_data.get("telephone"),
                password = self.validated_data.get("password"),
                otp_code=totp,
                secret_code=secret_code
            )

        return user
    
class LoginSerializer(TokenObtainPairSerializer):
    pass


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = [
            "email"
        ]

    def validate_email(self,value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email cannot be found")
        return value

    def _action_send(self):
        totp, secret_code = generate_otp()
        totp = totp.now()

        user = User.objects.get(email=self.validated_data.get("email"))
        email_sent = send_password_reset(username=user.username,email=user.email,otp_code=totp)

        if email_sent:
            user.otp_code = totp
            user.secret_code = secret_code
            user.save()
        return email_sent    
    
class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        fields = [
            "email","otp"
        ]

    def validate_email(self,value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email cannot be found")
        return value
    

    def validate(self, attrs):
        print(attrs)
        user = User.objects.get(email=attrs.get("email"))

        otp = attrs.get("otp")
        secret_code = user.secret_code
        
        is_verified = verify_otp(secret_code=secret_code,otp=otp)

        if not is_verified:
            raise serializers.ValidationError("OTP code is invalid")

        user.is_active = True
        user.save()

        return attrs

# class PasswordResetConfirmSerializer(VerifyOtpSerializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField()
#     new_password1 = serializers.CharField()
#     new_password2 = serializers.CharField()

#     class Meta:
#         fields = [
#             "email","otp","new_password1","new_password2"
#         ]

#         password1= self.attrs.get("password")
#         password2 = self.attrs.get("password2")

#         if password1 != password2:
#             return ValidationError(detail="password does not match")

#         return super().validate(attrs)


class PasswordChangeSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password1 = self.attrs.get("new_password1")
        new_password2 = self.attrs.get("new_password2")

        if new_password1 != new_password2:
            raise serializers.ValidationError("passwords are not the same")
        
        return super().validate(attrs)
    

class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()