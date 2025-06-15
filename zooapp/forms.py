from django import forms
from .models import Item
from django import template


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["nome", "especime", "data_coleta"]
        widgets = {
            "data_coleta": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        especime = cleaned_data.get("especime")
        data_coleta = cleaned_data.get("data_coleta")

        if not nome or not especime or not data_coleta:
            raise forms.ValidationError("Todos os campos são obrigatórios.")
