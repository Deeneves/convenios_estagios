from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Aluno, Curso, Faculdade

User = get_user_model()


class AcademicoFixturesTestCase(TestCase):
    """Teste que cria 10 alunos e 3 cursos no banco para uso em testes."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Cria 1 faculdade (necessária para os cursos)
        cls.faculdade = Faculdade.objects.create(nome="Faculdade de Teste")

        # Cria 3 cursos
        cls.cursos = []
        for i in range(1, 4):
            curso = Curso.objects.create(
                nome=f"Curso de Teste {i}",
                faculdade=cls.faculdade,
                duracao=8,
            )
            cls.cursos.append(curso)

        # Cria 10 usuários com role ALUNO
        cls.usuarios = []
        for i in range(1, 11):
            cpf = f"{i:011d}"  # CPF único: 00000000001, 00000000002, ...
            user = User.objects.create_user(
                cpf=cpf,
                password="senha123",
                email=f"aluno{i}@teste.edu.br",
                first_name=f"Aluno",
                last_name=f"Teste {i}",
                role=User.Role.ALUNO,
            )
            cls.usuarios.append(user)

        # Cria 10 alunos vinculados aos usuários (distribuídos entre os 3 cursos)
        cls.alunos = []
        for i, user in enumerate(cls.usuarios):
            curso = cls.cursos[i % 3]  # Alterna entre os 3 cursos
            aluno = Aluno.objects.create(
                user=user,
                curso=curso,
                matricula=f"202400{i+1:04d}",
                data_ingresso=date(2024, 1, 15),
                situacao=Aluno.Situacao.ATIVO,
            )
            cls.alunos.append(aluno)

    def test_fixtures_criados(self):
        """Verifica se os dados de teste foram criados corretamente."""
        self.assertEqual(Faculdade.objects.count(), 1)
        self.assertEqual(Curso.objects.count(), 3)
        self.assertEqual(User.objects.filter(role=User.Role.ALUNO).count(), 10)
        self.assertEqual(Aluno.objects.count(), 10)

    def test_alunos_tem_curso(self):
        """Verifica se todos os alunos têm curso associado."""
        for aluno in Aluno.objects.all():
            self.assertIsNotNone(aluno.curso)
            self.assertIn(aluno.curso, self.cursos)

    def test_cursos_tem_alunos(self):
        """Verifica se os cursos têm alunos associados."""
        total_alunos = sum(c.alunos.count() for c in self.cursos)
        self.assertEqual(total_alunos, 10)
