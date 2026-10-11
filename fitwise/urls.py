from django.urls import path
from fitwise.views import SignUpView,GetMeView
from fitwise.views import FoodLogListCreate,FoodLogRetrieveUpdateDeleteView

urlpatterns = [

    path('signup/',SignUpView.as_view()),
    path('me/',GetMeView.as_view()),
    path('foodlogs/',FoodLogListCreate.as_view()),
    path('foodlogs/<int:pk>/',FoodLogRetrieveUpdateDeleteView.as_view()),
]