from django.contrib.auth import models
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Currency, Category, Transaction
from .reports import ReportParams


class CurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class CategorySerializers(serializers.ModelSerializer):
    # Add user to associate Category to user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ("id", "name", "user")  # Add "user"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        read_only_fields = fields


class WriteTransactionSerializers(serializers.ModelSerializer):
    # use CurrentUserDefault to get user details
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

    # category = serializers.SlugRelatedField(slug_field="id", queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = ("id", "user", "amount", "description", "currency", "category", "created_at",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = user.categories.all()


class ReadTransactionSerializers(serializers.ModelSerializer):
    # queryset = Transaction.objects.select_related("currency","category","user")
    user = UserSerializer()
    currency = CurrencySerializers()
    category = CategorySerializers()

    class Meta:
        model = Transaction
        fields = ("id", "user", "amount", "description", "currency", "category", "created_at", "updated_at",)
        read_only_fields = fields


class ReportEntrySerializer(serializers.Serializer):
    category = CategorySerializers()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParametersSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    start_created_at = serializers.DateTimeField()
    end_created_at = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
