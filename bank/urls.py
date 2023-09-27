# urls.py in the bank app
from django.urls import path
from . import views

urlpatterns = [
    path('banks/', views.BankList.as_view(), name='bank-list'),
    path(
        'branches/<str:identifier>/',
        views.BranchDetail.as_view(), name='branch-detail'),
]
