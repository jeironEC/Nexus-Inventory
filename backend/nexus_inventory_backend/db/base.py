# Internal
import uuid

# Django
from django.db import models
from django.utils import timezone


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CLASS SOFT DELETE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CLASS MANAGER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CLASS AUDIT DATES
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class TimestampModel(models.Model):
    # Identifier
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])

    @property
    def is_deleted(self):
        return self.deleted_at is not None


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CLASS AUDIT AUTORS
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class AuditModel(TimestampModel):
    updated_by = models.ForeignKey(
        "db.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
    )
    deleted_by = models.ForeignKey(
        "db.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted_by",
    )

    class Meta:
        abstract = True


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CLASS BASE
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class BaseModel(AuditModel):
    # Autor
    created_by = models.ForeignKey(
        "db.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
    )

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.is_active = False
        self.save(update_fields=["deleted_at", "deleted_by", "updated_at", "is_active"])

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        self.is_active = True
        self.save(update_fields=["deleted_at", "deleted_by", "updated_at", "is_active"])


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CLASS DISPLAY MODEL
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class DisplayModel:
    def get_display_fields(self):
        return []

    def __str__(self):
        parts = []

        for field in self.get_display_fields():
            if callable(field):
                parts.append(str(field(self)))
            else:
                value = getattr(self, field, None)
                parts.append(str(value))

        return " - ".join(parts)
