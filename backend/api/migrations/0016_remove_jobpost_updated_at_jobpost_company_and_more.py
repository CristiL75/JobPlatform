# Generated by Django 4.1.13 on 2024-08-27 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_jobpost_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpost',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='jobpost',
            name='company',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='salary',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]