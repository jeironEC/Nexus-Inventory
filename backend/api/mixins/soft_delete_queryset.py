class SoftDeleteQuerysetMixin:
    """
    Aplica automáticamente deleted_at__isnull=True en querysets.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(deleted_at__isnull=True)
