from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']
        self.fields.keyOrder = ['email', 'password1', 'password2', 'alias', 'cell', 'carrier']
 
    class Meta:
        model = CustomUser
        fields = ("email","cell","carrier","alias")


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']
        self.fields.keyOrder = ['email', 'alias', 'cell', 'carrier']

    class Meta:
        model = CustomUser
        fields = ("email","cell","carrier","alias")


