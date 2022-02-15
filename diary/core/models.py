from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    class Meta:
        verbose_name_plural = "Currencies"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="currencies")
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transaction')

    def __str__(self):
        return f"{self.amount} - {self.description}"
