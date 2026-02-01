from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

# Classes Tailwind para os widgets
TAILWIND_INPUT = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
TAILWIND_SELECT = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"


class UserCreateForm(forms.ModelForm):
    """Formulário para cadastro de usuário (usado no fluxo de cadastro de aluno)."""

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Senha"}),
        min_length=8,
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Repita a senha"}),
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
                attrs={"class": TAILWIND_INPUT, "placeholder": "CPF (apenas números)", "maxlength": "11"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "Nome"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "Sobrenome"}
            ),
            "email": forms.EmailInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "E-mail"}
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


class AdminUserCreateForm(forms.ModelForm):
    """Formulário para cadastro de usuário pela administração."""

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Senha"}),
        min_length=8,
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Repita a senha"}),
        min_length=8,
    )

    class Meta:
        model = User
        fields = ["cpf", "first_name", "last_name", "email", "role"]
        labels = {
            "cpf": "CPF",
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "role": "Perfil",
        }
        widgets = {
            "cpf": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "CPF (apenas números)", "maxlength": "11"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "Nome"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "Sobrenome"}
            ),
            "email": forms.EmailInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "E-mail"}
            ),
            "role": forms.Select(attrs={"class": TAILWIND_SELECT}),
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
        if commit:
            user.save()
        return user


class AdminUserUpdateForm(forms.ModelForm):
    """Formulário para edição de usuário pela administração."""

    class Meta:
        model = User
        fields = ["cpf", "first_name", "last_name", "email", "role"]
        labels = {
            "cpf": "CPF",
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "role": "Perfil",
        }
        widgets = {
            "cpf": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "CPF (apenas números)", "maxlength": "11"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "Nome"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "Sobrenome"}
            ),
            "email": forms.EmailInput(
                attrs={"class": TAILWIND_INPUT, "placeholder": "E-mail"}
            ),
            "role": forms.Select(attrs={"class": TAILWIND_SELECT}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "").strip().replace(".", "").replace("-", "")
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError("Informe um CPF válido com 11 dígitos.")
        return cpf


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'CPF'
        self.fields['username'].widget.attrs['class'] = TAILWIND_INPUT
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password'].widget.attrs['class'] = TAILWIND_INPUT
