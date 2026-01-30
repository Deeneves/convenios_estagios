from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("academico", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aluno",
            name="data_ingresso",
            field=models.DateField(blank=True, null=True, verbose_name="Data de ingresso"),
        ),
    ]
