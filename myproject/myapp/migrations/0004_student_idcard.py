# Generated by Django 5.1.1 on 2024-10-04 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_remove_student_age"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="idCard",
            field=models.CharField(default=1234567891234, max_length=13),
            preserve_default=False,
        ),
    ]
