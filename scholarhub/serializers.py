from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token


class AdminRegistrationserializer(serializers.ModelSerializer):
    class Meta:
        model=Profiledb
        fields=["username","password","email"]

    
class StudentRegistrationserializer(serializers.ModelSerializer):
    class Meta:
        model=Profiledb
        fields=["username","first_name","last_name","email","password","phone","address"]



class CommonLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    otp_delivery_method = serializers.ChoiceField(choices=[('email', 'Email')])  # Removed 'phone' option

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        otp_delivery_method = data.get('otp_delivery_method')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid username or password')
            data['user'] = user
            data['otp_delivery_method'] = otp_delivery_method
        else:
            raise serializers.ValidationError('Must include "username" and "password"')

        return data

class VerifyOTPSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        otp = data.get('otp')

        if not username or not otp:
            raise serializers.ValidationError('Must include "username" and "otp"')

        return data



class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = [ 'name', 'description', 'eligibility', 'amount', 'duration', 'deadline']






from rest_framework import serializers
from .models import StudentApplication

class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = ['name', 'email', 'phone', 'certificate', 'identity', 'photo']

    def create(self, validated_data):
        student = self.context['student']
        scholarship = self.context['scholarship']
        return StudentApplication.objects.create(student=student, scholarship=scholarship, **validated_data)



        # read_only_fields=["id"]

class StudentApplicationSerializerUP(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = ['status'] 

        read_only_fields=["id"]

        



