from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response

from fitwise.serializers import UserSerializer,FoodLogSerializer
from fitwise.models import FoodLog
from fitwise.permissions import IsOwner

from datetime import datetime


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

class FoodLogSummaryView(APIView):

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data ={
            "today_total_calories":0
        }

        cur_date = datetime.now().date()

        cur_month = datetime.now().month

        cur_year = datetime.now().year

        #monthly transactions

        monthly_mealtypes = FoodLog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_mealtypes:
            
            monthly_total_calories=monthly_mealtypes.values("calorie").aggregate(total=Sum("calorie")).get("total")

            response_data["monthly_total_calories"]=monthly_total_calories

            #todays_calorie_summary

        todays_mealtype=FoodLog.objects.filter(owner=request.user,created_at__date=cur_date)

        if todays_mealtype:

            today_total_calories = todays_mealtype.values("calorie").aggregate(total=Sum("calorie")).get("total")

            # todays_category_summary

            category_summary = todays_mealtype.values("meal_type").annotate(total=Sum("calorie"))

            response_data["category_summary"]=category_summary

            response_data["today_total_calories"]=today_total_calories

        return Response(data=response_data)


class DietPlanView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        cur_month = datetime.now().month

        cur_year = datetime.now().year

        response_data={
            "monthly_total_calorie":0
        }

        monthly_food_entries = FoodLog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_food_entries:

            total_calorie = monthly_food_entries.values("meal_type").aggregate(total=Sum("calorie"))

            mealtype_summary = monthly_food_entries.values("meal_type").annotate(total=Sum("calorie"))

            response_data["total_calorie"]=total_calorie

            response_data["mealtype_summary"]=mealtype_summary

        return Response(data=response_data)    






  