# Django
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear

# DRF
from rest_framework.exceptions import ValidationError


def get_trunc_func(period):
    mapping = {
        "day": TruncDay,
        "week": TruncWeek,
        "month": TruncMonth,
        "year": TruncYear,
    }
    func = mapping.get(period)
    if not func:
        raise ValidationError(
            {"period": "Invalid period. Use day, week, month or year."}
        )
    return func
