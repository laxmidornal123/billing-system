from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):

    class Meta:

        model = Invoice

        fields = [
            'customer'
        ]

        widgets = {

            'customer': forms.Select(
                attrs={
                    'class':'form-select'
                }
            )

        }