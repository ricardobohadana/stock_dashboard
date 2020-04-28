from django.urls import path
from . import views


urlpatterns = [
    path('', views.homeView, name='homepage'),
    path('addstock/', views.newstockView, name='addstockpage'),
    path('updatestock/', views.updatestocksView, name='updatestockspage'),
    path('updatestock/<str:pk>', views.updatestockView, name='updatestockpage'),
    path('detailedstock/<str:pk>', views.detailedstockView, name='detailedstockpage'),
    path('removestock/<str:pk>', views.removestockView, name='removestockpage'),

]
