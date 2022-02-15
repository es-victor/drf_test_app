from rest_framework import status
from rest_framework.generics import CreateAPIView
from .reports import transaction_report
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Currency, Category, Transaction
from .serializers import CurrencySerializers, CategorySerializers, ReadTransactionSerializers, ReportEntrySerializer, \
    ReportParametersSerializer, WriteTransactionSerializers, RegisterUserSerializer


class CurrencyModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializers


class CategoryModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # queryset = Category.objects.all() # Delete this. to protect to only Auth user
    serializer_class = CategorySerializers

    # Add this. to protect to only Auth user
    def get_queryset(self):
        # # return only transactions belongs/associated with the user
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # queryset = Transaction.objects.select_related("currency", "category", "user")
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["description", "amount"]
    ordering_fields = ["amount", "created_at"]
    ordering = ['-created_at']
    filterset_fields = ["currency__code", "user__username", "category__id"]

    def get_queryset(self):
        # return only transactions belongs/associated with the user
        return Transaction.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializers
        return WriteTransactionSerializers

    #  Replaced by CurrentUserDefault on WriteTransactionSerializers
    # def perform_create(self, serializer):
    #     # add user id on create a transaction
    #     serializer.save(user=self.request.user)


class TransactionReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        params_serializer = ReportParametersSerializer(data=request.GET, context={"request": request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()

        data = transaction_report(params)
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(data=serializer.data)


class RegisterUserView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
