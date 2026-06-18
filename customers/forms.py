from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [
            'name',
            'mobile',
            'email',
            'address'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'mobile': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            )

        }