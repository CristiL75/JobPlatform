# Generated by Django 4.1.13 on 2024-08-27 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0014_remove_jobpost_created_by_jobpost_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]