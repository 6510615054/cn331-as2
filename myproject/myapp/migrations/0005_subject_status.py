# Generated by Django 5.1.1 on 2024-10-04 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_student_idcard"),
    ]

    operations = [
        migrations.AddField(
            model_name="subject",
            name="status",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
