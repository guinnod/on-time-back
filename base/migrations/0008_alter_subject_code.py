# Generated by Django 4.2.1 on 2023-05-10 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_user_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=70, unique=True),
        ),
    ]
