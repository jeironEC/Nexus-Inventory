# Django
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth

# DRF
from rest_framework.exceptions import ValidationError


def get_trunc_func(period):
    mapping = {
        "day": TruncDay,
        "week": TruncWeek,
        "month": TruncMonth,
    }
    func = mapping.get(period)
    if not func:
        raise ValidationError({"period": "Invalid period. Use day, week or month."})
    return func
