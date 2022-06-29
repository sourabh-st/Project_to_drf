from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import MyProfile, MyPost
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from .serializers import MyProfileSerializer, MyPostListSerializer, LoginSerializer,PostCreateSerializer,FollowSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
test_param = openapi.Parameter('Authorization', openapi.IN_HEADER, description="test manual param", type=openapi.TYPE_STRING)
# Create your views here.

###################  SIGN-UP   #############################################

class Signup(APIView):

    @swagger_auto_schema(operation_description='Sign up', request_body=MyProfileSerializer)
    def post(self, request):
        postData = request.data
        first_name = postData.get('first_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        address = postData.get('address','')
        age = postData.get('age','')
        stat = postData.get('stat','')
        gender = postData.get('gender','')
        try:
            user = User.objects.create_user(username = phone, email=email,password=password)
            user.set_password(password)
            user.save()
            MyProfile.objects.create(user=user,profilename=first_name, age=age , address = address,stat=stat,gender=gender)

        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                "Success" : True,
                "msg" : "Registration Done!",
            }, status=status.HTTP_200_OK)

############################---LOGIN---########################


class Login(APIView):

    @swagger_auto_schema(operation_description='Login', request_body=LoginSerializer)
    def post(self,request):
        data = request.data
        phone = data.get('phone')
        password = data.get('password')
        user_object = authenticate(username=phone, password=password)
        if user_object is not None:
            refresh = RefreshToken.for_user(user_object)
            return Response({
                "Success" : True,
                "msg" : "Logged in!",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "Success" : False,
                    'msg': 'Login Failed!!'
            }, status=status.HTTP_404_NOT_FOUND)


class ProfileGet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='Get profile',manual_parameters=[test_param])
    def get(self, request):
        try:
            profile_object,_ = MyProfile.objects.get_or_create(user=request.user)
            print(profile_object)
            serializer = MyProfileSerializer(profile_object)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                "Success" : True,
                    'msg': 'Profile Fetched!',
                    'user_data': serializer.data
            }, status=status.HTTP_200_OK)


class MyPostCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='Create Post',manual_parameters=[test_param] , request_body=PostCreateSerializer)
    def post(self, request):
        try:
            data = request.data
            post_object =  MyPost.objects.create(**data)
            post_object.uploaded_by = request.user
            post_object.save()
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
                "Success" : True,
                    'msg': 'Post Created!',
            }, status=status.HTTP_200_OK)

class MyPostList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='My Post List',manual_parameters=[test_param])
    def get(self, request):
        post_objects = MyPost.objects.filter(uploaded_by = self.request.user).order_by("-id")
        serializer = MyPostListSerializer(post_objects, many=True, context={"request": request})
        print(post_objects)
        print(serializer.data)
        return Response({
                "Success" : True,
                    'msg': 'Post Listed!',
                    'user_data': serializer.data
            }, status=status.HTTP_200_OK)



class Connections(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='Connections',manual_parameters=[test_param])
    def get(self,request):
        followings = []
        suggestions = []
        followers = []
        my_followings = []
        if request.user.is_authenticated:
            followings = MyProfile.objects.filter(followers=request.user).values_list('user', flat=True)
            suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).exclude(is_superuser = True).order_by("-id")
            print("suggestions: ", suggestions)
            print("followings: ", followings)
            
            try:
                
                user_follower_object = MyProfile.objects.get(user = request.user)
            except MyProfile.DoesNotExist:
                user_follower_object = MyProfile.objects.create(user = request.user)
            
            followers = user_follower_object.followers.all()
            print("followers: " , followers)

            my_followings = User.objects.filter(pk__in=followings)
            print("my_followings",my_followings)
            
            serializer = MyProfileSerializer(followers)
            print(serializer.data)

        return Response({
                    "Success" : True,
                        'msg':'Followers List Loaded Sucessfully!!',
                        # 'suggestions': suggestions,
                        # 'followers' : followers,
                        # 'my_followings' : my_followings

                }, status=status.HTTP_200_OK)

class Follow(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='Follow',manual_parameters=[test_param], request_body=FollowSerializer)
    def post(self, request):
        postData = request.data
        id = postData.get('id')
        try:
            user_to_follow = User.objects.get(id=id)
            user = MyProfile.objects.get(user = request.user)
            user.followers.add(user_to_follow)
            user.save()
            return Response({
                    "Success" : True,
                        "msg":"Followed Successfully!"
                }, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                    "Success" : False,
                    "msg" : str(e)
                }, status=status.HTTP_400_BAD_REQUEST)