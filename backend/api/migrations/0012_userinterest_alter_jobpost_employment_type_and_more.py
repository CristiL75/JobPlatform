# Generated by Django 4.1.13 on 2024-08-27 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0011_jobpost_employment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='employment_type',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Interest',
        ),
        migrations.AddField(
            model_name='userinterest',
            name='job_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.jobpost'),
        ),
        migrations.AddField(
            model_name='userinterest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]