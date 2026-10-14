from django.urls import path
from fitwise.views import SignUpView,GetMeView
from fitwise.views import FoodLogListCreate,FoodLogRetrieveUpdateDeleteView
from fitwise.views import FoodLogSummaryView
from fitwise.views import DietPlanView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [

    path('signup/',SignUpView.as_view()),
    path('me/',GetMeView.as_view()),
    path('foodlogs/',FoodLogListCreate.as_view()),
    path('foodlogs/<int:pk>/',FoodLogRetrieveUpdateDeleteView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
    path('foodlogs/summary/',FoodLogSummaryView.as_view()),
    path("dietplan/",DietPlanView.as_view()),
]