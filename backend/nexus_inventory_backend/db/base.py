# Internal
import uuid

# Django
from django.db import models
from django.utils import timezone


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CLASS MANAGER
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
class ActiveManager(models.Manager):
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

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
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
        self.save(update_fields=["deleted_at", "deleted_by", "updated_at"])
