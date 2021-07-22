# Generated by Django 3.2.5 on 2021-07-17 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20210717_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todo',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Collaborator',
        ),
    ]