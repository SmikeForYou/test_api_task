from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from user.models import User


class UserCreationForm(UserCreationForm):
    """
    A form that creats a custom user with no privilages
    form a provided email and password.
    """

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        self.fields.pop("username", None)

    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)
        self.fields.pop("username", None)

    class Meta:
        model = User
        fields = "__all__"
