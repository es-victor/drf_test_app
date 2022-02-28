from unicodedata import name
from django.urls import path
from .views import TransactionModelViewSet, CategoryModelViewSet, CurrencyModelViewSet, TransactionReportAPIView, \
    RegisterUserView, LogoutView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'categories', CategoryModelViewSet, basename="category")
router.register(r'currencies', CurrencyModelViewSet, basename="currency")
router.register(r'transactions', TransactionModelViewSet, basename="transaction")

urlpatterns = [
                path("report/", TransactionReportAPIView.as_view(), name="report"),
                path("register/", RegisterUserView.as_view(), name="register"),
                path("logout/", LogoutView.as_view(), name="logout")
              ] + router.urls
