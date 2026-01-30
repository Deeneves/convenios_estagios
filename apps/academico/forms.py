from django import forms
from django.contrib.auth import get_user_model

from .models import Aluno, Curso, Faculdade

User = get_user_model()

# Classes Tailwind para os widgets
TAILWIND_INPUT = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
TAILWIND_SELECT = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"


class FaculdadeForm(forms.ModelForm):
    class Meta:
        model = Faculdade
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Nome da faculdade"}),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nome", "faculdade", "duracao"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Nome do curso"}),
            "faculdade": forms.Select(attrs={"class": TAILWIND_SELECT}),
            "duracao": forms.NumberInput(attrs={"class": TAILWIND_INPUT, "min": 1, "placeholder": "Semestres"}),
        }


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            "user",
            "curso",
            "matricula",
            "situacao",
            "data_nascimento",
            "rg",
            "estado_civil",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "cep",
        ]
        widgets = {
            "user": forms.Select(attrs={"class": TAILWIND_SELECT}),
            "curso": forms.Select(attrs={"class": TAILWIND_SELECT}),
            "matricula": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Matrícula"}),
            "situacao": forms.Select(attrs={"class": TAILWIND_SELECT}),
            "data_nascimento": forms.DateInput(attrs={"class": TAILWIND_INPUT, "type": "date"}),
            "rg": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "RG"}),
            "estado_civil": forms.Select(attrs={"class": TAILWIND_SELECT}),
            "logradouro": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Logradouro"}),
            "numero": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Número"}),
            "complemento": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Complemento"}),
            "bairro": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Bairro"}),
            "cidade": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Cidade"}),
            "estado": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "UF", "maxlength": "2"}),
            "cep": forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "CEP"}),
        }

    def __init__(self, *args, **kwargs):
        user_preenchido_id = kwargs.pop("user_preenchido_id", None)
        super().__init__(*args, **kwargs)
        if user_preenchido_id:
            # Fluxo vindo do cadastro de usuário: usuário já definido, campo oculto
            self.fields["user"].widget = forms.HiddenInput()
            self.fields["user"].initial = user_preenchido_id
            self.fields["user"].queryset = User.objects.filter(pk=user_preenchido_id)
        else:
            # Apenas usuários que ainda não têm vínculo com aluno (ao editar, inclui o próprio usuário)
            from .models import Aluno as AlunoModel
            usuarios_com_aluno = list(AlunoModel.objects.values_list("user_id", flat=True))
            if self.instance and self.instance.pk and self.instance.user_id:
                usuarios_com_aluno = [pk for pk in usuarios_com_aluno if pk != self.instance.user_id]
            self.fields["user"].queryset = User.objects.exclude(pk__in=usuarios_com_aluno).order_by("first_name", "username")
