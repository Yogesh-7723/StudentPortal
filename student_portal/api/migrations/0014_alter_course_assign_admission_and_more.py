# Generated by Django 5.2 on 2025-04-11 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_course_assign_expire_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_assign',
            name='admission',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 11, 20, 49, 18, 722299)),
        ),
        migrations.AlterField(
            model_name='course_assign',
            name='expire_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 11, 20, 49, 18, 722299)),
        ),
    ]
