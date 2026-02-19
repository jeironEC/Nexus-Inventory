# Django
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Base model


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and saves a User with the given email and password.
        """

        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superiser must hava is_staff on True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superiser must hava is_superuser on True.")

        admin_role, _ = Role.objects.get_or_create(
            name="ADMIN", defaults={"description": "Administrator role"}
        )

        extra_fields.setdefault("role", admin_role)

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")

    updated_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_active", "deleted_at"])
