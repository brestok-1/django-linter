# Generated by Django 4.2.4 on 2023-08-24 19:14

import checker.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=checker.models.upload_to, validators=[checker.models.validate_file_extension])),
                ('filename', models.CharField(max_length=64, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Новый', 'New'), ('Удален', 'Deleted'), ('Перезаписан', 'Overwritten')], default='Новый', max_length=20)),
                ('check_result', models.TextField(default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
