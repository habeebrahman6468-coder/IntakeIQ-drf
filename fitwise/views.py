from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from fitwise.serializers import UserSerializer,FoodLogSerializer
from fitwise.models import FoodLog
from fitwise.permissions import IsOwner


# Create your views here.


class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data = form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance.validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializer(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class GetMeView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username = auth_user)

        serializer_instance= UserSerializer(instance)

        return Response(data=serializer_instance.data)

class FoodLogListCreate(APIView):

    authentication_classes =[ authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        instance = FoodLog.objects.filter(owner= request.user)

        serializer_instance = FoodLogSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data 

        serializer_instance = FoodLogSerializer(data= form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner = request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class FoodLogRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = FoodLogSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data 

        serializer_instance = FoodLogSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data= serializer_instance.data)

        else:

            return Response(data= serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"FoodLog deleted..."})     