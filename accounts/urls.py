from django.urls import path
from . import views



urlpatterns = [
    path('', views.newhomeView, name='homepage'),
    path('addstock/', views.newstockView, name='addstockpage'),
    path('updatestock/', views.updatestocksView, name='updatestockspage'),
    path('detailedstock/<str:pk>', views.detailedstockView, name='detailedstockpage'),
    path('removestock/<str:pk>', views.removestockView, name='removestockpage'),
    path('forex/', views.forexView.as_view(), name='forexpage'),
    path('wallet/', views.WalletView.as_view(), name='walletpage'),
    path('wallet/create', views.createWalletView.as_view(), name='createwalletpage'),
    path('wallet/update', views.updateWalletView.as_view(), name='updatewalletpage'),
    path('wallet/delete', views.deleteWalletView.as_view(), name='deletewalletpage'),
]
