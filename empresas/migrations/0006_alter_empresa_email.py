# Generated by Django 4.1.3 on 2022-11-09 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0005_alter_vagas_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
