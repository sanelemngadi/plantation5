# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PlantationUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = PlantationUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

        widgets = {
            "as_admin": forms.TextInput(attrs={"placeholder": "please enter your employement id"})
        }

class RadioSelectWidget(forms.widgets.Widget):
    template_name = 'radio.html'  # You can customize the template for your radio buttons

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_radio'] = True  # Add a flag to distinguish radio buttons
        return context


class PlantationUpdateUserForm(forms.ModelForm):
    class Meta:
        model = PlantationUser
        fields = ("role",)

        widgets = {
            "role": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(PlantationUpdateUserForm, self).__init__(*args, **kwargs)

        # Set the empty_label to None for the select field
        self.fields['role'].choices = PlantationUser.ROLE

