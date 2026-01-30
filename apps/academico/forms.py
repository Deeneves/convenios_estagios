from django import forms
from django.contrib.auth import get_user_model

from .models import Aluno, Curso, Faculdade

User = get_user_model()


class FaculdadeForm(forms.ModelForm):
    class Meta:
        model = Faculdade
        fields = ["nome"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome da faculdade"}),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nome", "faculdade", "duracao"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do curso"}),
            "faculdade": forms.Select(attrs={"class": "form-select"}),
            "duracao": forms.NumberInput(attrs={"class": "form-control", "min": 1, "placeholder": "Semestres"}),
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
            "user": forms.Select(attrs={"class": "form-select"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "matricula": forms.TextInput(attrs={"class": "form-control", "placeholder": "Matrícula"}),
            "situacao": forms.Select(attrs={"class": "form-select"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "rg": forms.TextInput(attrs={"class": "form-control", "placeholder": "RG"}),
            "estado_civil": forms.Select(attrs={"class": "form-select"}),
            "logradouro": forms.TextInput(attrs={"class": "form-control", "placeholder": "Logradouro"}),
            "numero": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número"}),
            "complemento": forms.TextInput(attrs={"class": "form-control", "placeholder": "Complemento"}),
            "bairro": forms.TextInput(attrs={"class": "form-control", "placeholder": "Bairro"}),
            "cidade": forms.TextInput(attrs={"class": "form-control", "placeholder": "Cidade"}),
            "estado": forms.TextInput(attrs={"class": "form-control", "placeholder": "UF", "maxlength": "2"}),
            "cep": forms.TextInput(attrs={"class": "form-control", "placeholder": "CEP"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apenas usuários que ainda não têm vínculo com aluno (ao editar, inclui o próprio usuário)
        from .models import Aluno as AlunoModel
        usuarios_com_aluno = list(AlunoModel.objects.values_list("user_id", flat=True))
        if self.instance and self.instance.pk and self.instance.user_id:
            usuarios_com_aluno = [pk for pk in usuarios_com_aluno if pk != self.instance.user_id]
        self.fields["user"].queryset = User.objects.exclude(pk__in=usuarios_com_aluno).order_by("first_name", "username")
