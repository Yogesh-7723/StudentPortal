# Generated by Django 5.2 on 2025-04-09 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_assign_submit_assignment_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign_submit',
            name='check_by',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='assign_submit',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
