# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.viewsets import ViewSet
# from .serializers import *
# from .models import *
# from django.http import Http404
# from rest_framework import status
# from django.contrib.auth import login,logout
# from rest_framework.authtoken.models import Token
# from scholarhub.models import Profiledb 
# from rest_framework import authentication,permissions
# from django.conf import settings
# from django.utils import timezone
# from datetime import timedelta
# import random
# import string
# import phonenumbers
# from django.core.mail import send_mail
# # from twilio.rest import Client
# from .sms_utils import send_otp_via_sms

import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
# from .sms_utils import send_otp_via_sms
# import phonenumbers
# import firebase_admin
# from firebase_admin import auth as firebase_auth




# def superuser(fn):

#     def wrapper(request,*args,**kwargs):
#         if request.user.is_superuser:
#             return fn(request,*args,**kwargs)
#         else:
#             print("get out")
#     return wrapper
# Create your views here.
class AdminRegistrationview(APIView):
    serializer_class=AdminRegistrationserializer
    def post(self,request):
        serializer=AdminRegistrationserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["is_admin"]=True
            user=Profiledb.objects.create_user(**serializer.validated_data)
            return Response({'msg':'admin registered succcessfully'},status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class StudentRegistrationView(APIView):
    serializer_class=StudentRegistrationserializer
    def post(self,request):
        serializer=StudentRegistrationserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['is_student']=True
            user=Profiledb.objects.create_user(**serializer.validated_data)
            return Response({'msg':'student registered successfully'},status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class LoginAPI(APIView):
    serializer_class = CommonLoginSerializer

    def post(self, request):
        serializer = CommonLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp_delivery_method = serializer.validated_data['otp_delivery_method']
            
            # Generate normal-number OTP
            otp = ''.join(random.choices(string.digits, k=6))
            user.otp = otp
            user.otp_expiry = timezone.now() + timedelta(minutes=1)
            user.save()

            try:
                # Send OTP via email
                if otp_delivery_method == 'email':
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp}',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    message = 'OTP sent to your email.'
                    
                # For phone OTP, you would have a similar logic to send via SMS
                    
            except Exception as e:
                return Response({'message': f'Failed to send OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': message}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPAPI(APIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            otp = serializer.validated_data['otp']
            user = Profiledb.objects.filter(username=username).first()

            if user and user.otp == otp and user.otp_expiry > timezone.now():
                user.otp = None
                user.otp_expiry = None
                user.save()

                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'id': user.id,
                    'username': user.username,
                    'is_student': user.is_student,
                    'is_admin': user.is_admin,
                }

                return Response({'message': 'Logged in successfully', 'token': token.key, 'data': data}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
 
# class AddScholarship(APIView):
#      def post(self,request,*args,**kwargs):
#          serializer=ScholarshipSerializer(data=request.data)
#          if serializer.is_valid():
#              serializer.save()
#              return Response(data=serializer.data)
#          else:
#              return Response(serializer.errors)

# class AddScholarship(APIView):  # view for admin to add scholarship
#     def post(self, request, *args, **kwargs):
#         if request.user.is_superuser:
#         # Retrieve the logged-in user
#         # user = request.user
#          message_data = {
#             'name':  request.data.get('name',request.data),
#             'description': request.data.get('description',request.data),
#             'eligibility':  request.data.get('eligibility',request.data),
#             'amount': request.data.get('amount',request.data),
#             'user': request.user.id,
#             'duration': request.data.get('duration',request.data),
#             'deadline': request.data.get('deadline',request.data)

#          }
#         else:
#             print("get out")
        
        
#         serializer = ScholarshipSerializer(data=message_data)
        
#         if serializer.is_valid():
#                 serializer.save()
#                 return Response(data=serializer.data)
#         else:
#                 return Response(serializer.errors)
class AddScholarshipView(APIView):
    def post(self, request):
        if request.user.is_superuser:
        # Get data from the request
         message_data = request.data
        else:
            print("get out")

        # Initialize the serializer with the data
        serializer = ScholarshipSerializer(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():
            # Save the valid data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return the errors if the data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class ListScholarshipforadmin(APIView): # view for list all scholarship by admin

    def get(self, request, *args, **kwargs):
        

        # Retrieve projects uploaded by the currently authenticated user
         projects = Scholarship.objects.all()
         serializer = ScholarshipSerializer(projects, many=True)
         return Response(serializer.data)
    



# class ViewAppliedStudents(APIView):
#     def list (self,request,*args,**kwargs):
#         list=StudentApplication.objects.all()
#         serializer=StudentApplicationSerializer(list,many=True)
#         return Response(serializer.data)

class Admin_stud_ApplicationView(ViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list (self,request,*args,**kwargs):
        list=StudentApplication.objects.all()
        serializer=StudentApplicationSerializer(list,many=True)
        return Response(serializer.data)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        list=StudentApplication.objects.get(id=id)
        serializer=StudentApplicationSerializer(list)
        return Response(serializer.data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=StudentApplication.objects.get(id=id)
        serializers=StudentApplicationSerializerUP(data=request.data,instance=qs)
        if serializers.is_valid():
            serializers.save()
            print(qs.scholarship.amount)
            amount=qs.scholarship.amount
            email=qs.email
            print(email)
            subject='status'
            if qs.status=="rejected":
                message=f'hii ur status has been rejected'
            else:
                if qs.scholarship:
                    amount = qs.scholarship.amount
                else:
                    amount = 'N/A'

                message = f'Hi, your application status has been accepted. The amount approved is {amount}.'

            email_from= settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject,message,email_from,recipient_list)
            


            return Response(data=serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

    

    
    













#student side






class StudentApply(APIView):
    def post(self, request, *args, **kwargs):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Ensure Profiledb instance exists and has required fields
        try:
            student_profile = Profiledb.objects.get(pk=request.user.pk)
            if not student_profile.address:
                return Response({"error": "User profile address is missing"}, status=status.HTTP_400_BAD_REQUEST)
        except Profiledb.DoesNotExist:
            return Response({"error": "Profiledb instance not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)

        # Populate message_data with the Profiledb instance
        message_data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'student': student_profile.id,
            'application_date': request.data.get('application_date'),
            'certificate': request.data.get('certificate'),
            'identity': request.data.get('identity'),
            'photo': request.data.get('photo'),
            'scholarship': request.data.get('scholarship')
        }

        # Serialize and save the StudentApplication instance
        serializer = StudentApplicationSerializer(data=message_data)
        if serializer.is_valid():
            user=serializer.validated_data['student']=request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class ListScholarshipforStudents(APIView): # view for list all scholarship for  students

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def get(self, request, *args, **kwargs):
        # Retrieve projects uploaded by the currently authenticated user
        projects = Scholarship.objects.all()
        serializer = ScholarshipSerializer(projects, many=True)
        return Response(serializer.data)
    

class ViewAppliedScholarship(APIView): #to view each students applied list of scholarship
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=StudentApplication.objects.filter(student=id)
        serializer = StudentApplicationSerializer(qs, many=True)
        return Response(serializer.data)
    
    # def get(self,request,*args,**kwargs):

    #     qs=StudentApplication.objects.all()
    #     serializer = StudentApplicationSerializer(qs, many=True)
    #     return Response(serializer.data)

    


    




    # def get(self, request, *args, **kwargs):  # fuction for list each shoclarship
    #     id=kwargs.get("pk")
    #     Scholarship = Scholarship.objects.filter(id=id)
    #     serializer = Scholarship(Scholarship, many=True)
    #     return Response(serializer.data)

class RetrieveScholarship(APIView):  # to view each scholarship one by one for students

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        qs=Scholarship.objects.get(id=id)

        serializer=ScholarshipSerializer(qs)

        return Response(serializer.data)
    
    
    def put(self,request,*args,**kwargs): #only for admin

        id=kwargs.get('pk')
        if request.user.is_superuser:
            qs=Scholarship.objects.filter(scholarship_id=id)
            serializer=ScholarshipSerializer(data=request.data,instance=qs)
            if serializer.is_valid():
                serializer.save()
            return Response(data=serializer.data)
        else:
            print("get out")

         

         
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Scholarship, Profiledb, StudentApplication
from .serializers import StudentApplicationSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applicationform(request, scholar_id):
    scholar = get_object_or_404(Scholarship, pk=scholar_id)
    student = get_object_or_404(Profiledb, pk=request.user.pk)

    if request.method == 'POST':
        serializer = StudentApplicationSerializer(data=request.data, context={'student': student, 'scholarship': scholar})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
