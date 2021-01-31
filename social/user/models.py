from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from core import mixins as core_mixins
from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    first_name = models.CharField("first_name", max_length=30, blank=True)
    middle_name = models.CharField("middle_name", max_length=30, blank=True)
    last_name = models.CharField("last_name", max_length=30, blank=True)
    date_joined = models.DateTimeField("date_joined", auto_now_add=True)
    is_active = models.BooleanField("active", default=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    @property
    def is_staff(self):
        """
        Only admin can access admin panel
        """
        return self.is_superuser

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        pass

    @property
    def last_activity(self):
        return UserActivity.get_last_user_action(self)



class UserActivity(core_mixins.DateAddedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=64)

    @classmethod
    def get_last_user_action(cls, user):
        last_action = cls.objects.filter(user=user).order_by("-date_created").first()
        return last_action.date_created