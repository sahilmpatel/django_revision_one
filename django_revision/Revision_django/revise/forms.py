from django import forms
from .models import Banks
class details(forms.Form):
    name = forms.CharField(label='Name',max_length=50)
    email = forms.EmailField(label='Email')

class file_upload(forms.Form):
    file = forms.FileField()

class BankForm(forms.ModelForm):
    class Meta:
        model = Banks
        fields = "__all__"