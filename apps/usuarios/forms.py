from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    """Formulário para cadastro de usuário (usado no fluxo de cadastro de aluno)."""

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"}),
        min_length=8,
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repita a senha"}),
        min_length=8,
    )

    class Meta:
        model = User
        fields = ["cpf", "first_name", "last_name", "email"]
        labels = {
            "cpf": "CPF",
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
        }
        widgets = {
            "cpf": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "CPF (apenas números)", "maxlength": "11"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Sobrenome"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "E-mail"}
            ),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "").strip().replace(".", "").replace("-", "")
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError("Informe um CPF válido com 11 dígitos.")
        return cpf

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = User.Role.ALUNO
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'CPF'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'