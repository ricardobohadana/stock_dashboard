from django.urls import path, include
from . import views



urlpatterns = [
    # -------------------------------- WEB URLS -------------------------------------------
    path('', views.newhomeView.as_view(), name='homepage'),
    path('query/', views.queryView.as_view(), name='querypage'),
    path('bvsp/', views.bvspView.as_view(), name='ibovpage'),
    path('addstock/', views.newstockView, name='addstockpage'),
    path('detailedstock/<str:pk>', views.detailedstockView, name='detailedstockpage'),
    path('removestock/<str:pk>', views.removestockView, name='removestockpage'),
    path('forex/', views.forexView.as_view(), name='forexpage'),
    path('wallet/', views.WalletView.as_view(), name='walletpage'),
    path('wallet/create', views.createWalletView.as_view(), name='createwalletpage'),
    path('wallet/update', views.updateWalletView.as_view(), name='updatewalletpage'),
    path('wallet/delete', views.deleteWalletView.as_view(), name='deletewalletpage'),
]
