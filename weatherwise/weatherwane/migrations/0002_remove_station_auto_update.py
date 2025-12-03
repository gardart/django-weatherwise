from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("weatherwane", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="station",
            name="auto_update",
        ),
    ]
