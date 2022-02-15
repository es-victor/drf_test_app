from dataclasses import dataclass
import datetime
from decimal import Decimal
from .models import Category, Transaction
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg


@dataclass
class ReportEntry:
    category: Category
    total: Decimal
    count: int
    avg: Decimal


@dataclass()
class ReportParams:
    start_created_at = datetime.datetime
    end_created_at = datetime.datetime
    user = User


def transaction_report(params: ReportParams):
    data = []

    queryset = Transaction.objects.filter(
        created_at__gte=params.start_created_at,
        created_at__lte=params.end_created_at,
        user=params.user
    ).values("category").annotate(
        total=Sum("amount"),
        count=Count("id"),
        avg=Avg("amount")
    )

    categories_index = {}
    for category in Category.objects.all():
        categories_index[category.pk] = category

    for entry in queryset:
        category = categories_index.get(entry["category"])
        report_entry = ReportEntry(category, entry["total"], entry["count"], entry["avg"])
        data.append(report_entry)
    return data
