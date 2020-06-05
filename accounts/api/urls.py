from accounts.api.serializers import StockSerializer, WalletSerializer
from accounts.api import views
from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------- API URLS -------------------------------------------
    # Stock model
    path('', views.ApiOverview.as_view(), name='apiinfopage'),
    path('stock/', views.StockApiView.as_view(), name='apistockpage'),
    path('stock/<str:id>', views.StockApiDetailView.as_view(), name='apistockdetailpage'),
    # path('stock/create', views.StockAPIView.as_view(), name='apistockcreatepage'),
    path('stock/update/', views.StockApiUpdateView.as_view(), name='apistockupdatepage'),
    # path('stock/delete/<str:pk>', views.apiOverview.as_view(), name='apistockdeletepage'),
    
    # # Wallet model
    path('wallet/', views.WalletApiView.as_view(), name='apiwalletpage'),
    # path('wallet/create/', views.apiOverview.as_view(), name='apiwalletcreatepage'),
    path('wallet/update/', views.WalletApiUpdateView.as_view(), name='apiwalletupdatepage'),
    # path('wallet/delete/<str:pk>', views.WalletApiDeleteView.as_view(), name='apiwalletdeletepage'),
]
