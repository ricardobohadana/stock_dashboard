from django.urls import path
from . import views



urlpatterns = [
    path('', views.newhomeView, name='homepage'),
    path('addstock/', views.newstockView, name='addstockpage'),
    path('updatestock/', views.updatestocksView, name='updatestockspage'),
    path('detailedstock/<str:pk>', views.detailedstockView, name='detailedstockpage'),
    path('removestock/<str:pk>', views.removestockView, name='removestockpage'),
    path('wallet/', views.walletView, name='walletpage'),
]
