# Generated by Django 5.0.4 on 2024-05-14 01:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('WORK', 'Work'), ('PERSONAL', 'Personal'), ('OTHERS', 'Others')], default='PERSONAL', max_length=20)),
                ('status', models.CharField(choices=[('TO DO', 'To Do'), ('IN PROGRESS', 'In Progress'), ('DONE', 'Done')], default='TO DO', max_length=20)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to=settings.AUTH_USER_MODEL)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
