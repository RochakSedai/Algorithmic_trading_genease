from django.urls import path
from . import views
from .views import plot_before\

urlpatterns = [
    path('', views.home, name='home'),
    path('backtest', views.backtest, name='backtest'),
    path('plot_after', views.plot_after, name='plot_after'),
    path('plot_before', plot_before.as_view(), name='plot_before'),
]