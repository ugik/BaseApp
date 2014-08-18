from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from models import CustomUser
import string

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
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['email'].widget.attrs['readonly'] = True
        del self.fields['username']
        self.fields.keyOrder = ['email', 'alias', 'cell', 'carrier']
        readonly_fields = ('email',)

    class Meta:
        model = CustomUser
        fields = ("email","cell","carrier","alias")

    def clean_cell(self):    # strip non-numerics out of cell #
        cell = self.cleaned_data['cell']
        self.cleaned_data['cell'] = filter(lambda c: c in string.digits + '', cell)
        return self.cleaned_data['cell']


