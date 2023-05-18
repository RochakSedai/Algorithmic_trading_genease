from django.urls import path
from . import views
from .views import plot_before\

urlpatterns = [
    path('', views.home, name='home'),
    path('backtest', views.backtest, name='backtest'),
]