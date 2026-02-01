import re
from datetime import timedelta

from django import forms

from .models import Encaminhamento, Horas, Secretaria

# Classes Tailwind para os widgets
TAILWIND_INPUT = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
TAILWIND_SELECT = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"


class SecretariaForm(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ["nome", "sigla"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Nome da secretaria"}),
            "sigla": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Sigla"}),
        }


class EncaminhamentoForm(forms.ModelForm):
    class Meta:
        model = Encaminhamento
        fields = ["secretaria", "aluno"]
        widgets = {
            "secretaria": forms.Select(attrs={"class": TAILWIND_SELECT}),
            "aluno": forms.Select(attrs={"class": TAILWIND_SELECT}),
        }


class HorasForm(forms.ModelForm):
    quantidade = forms.CharField(
        label="Quantidade de horas",
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "HH:MM"}),
    )

    class Meta:
        model = Horas
        fields = [
            "aluno",
            "quantidade",
            "oficio_informacao",
            "oficio_documento",
        ]
        widgets = {
            "aluno": forms.Select(attrs={"class": TAILWIND_SELECT}),
            "oficio_informacao": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Número do ofício"}),
            "oficio_documento": forms.ClearableFileInput(attrs={"class": TAILWIND_INPUT}),
        }

    def clean_quantidade(self):
        valor = (self.cleaned_data.get("quantidade") or "").strip()
        if not re.match(r"^\d{1,2}:\d{2}$", valor):
            raise forms.ValidationError("Informe as horas no formato HH:MM.")
        horas, minutos = valor.split(":")
        horas_int = int(horas)
        minutos_int = int(minutos)
        if minutos_int > 59:
            raise forms.ValidationError("Minutos devem ser entre 00 e 59.")
        return timedelta(hours=horas_int, minutes=minutos_int)
