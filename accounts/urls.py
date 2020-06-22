from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # -------------------------------- WEB URLS -------------------------------------------
    path('', views.newhomeView.as_view(), name='homepage'),
    path('query/', views.queryView.as_view(), name='querypage'),
    path('bvsp/', views.bvspView.as_view(), name='ibovpage'),
    path('addstock/', views.newstockView, name='addstockpage'),
    path('detailedstock/<str:pk>', views.detailedstockView, name='detailedstockpage'),
    path('removestock/<str:pk>', views.removestockView, name='removestockpage'),
    path('forex/', views.forexView.as_view(), name='forexpage'),
    path('transactions/', views.transactionView.as_view(), name='transactionspage'),
    path('wallet/', views.WalletView.as_view(), name='walletpage'),
    path('wallet/create', views.createWalletView.as_view(), name='createwalletpage'),
    path('wallet/update', views.updateWalletView.as_view(), name='updatewalletpage'),
    path('wallet/delete', views.deleteWalletView.as_view(), name='deletewalletpage'),
    path('wallet/summary/<str:id>', views.InvestmentSummary.as_view(), name='summarypage'),
    path('wallet/summary/<str:id>/transactions', views.TransactionSummary.as_view(), name='summarytransactionspage'),
    path('wallet/summary/<str:id>/stocks', views.StocksSummary.as_view(), name='summarystockspage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
