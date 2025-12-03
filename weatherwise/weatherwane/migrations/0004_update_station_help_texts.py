from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weatherwane", "0003_make_station_name_code_required"),
    ]

    operations = [
        migrations.AlterField(
            model_name="station",
            name="name",
            field=models.CharField(
                default="",
                help_text="Required station name (e.g., Akureyri)",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="station",
            name="code",
            field=models.CharField(
                default="",
                help_text="Required station code from the XML feed (e.g., 3471)",
                max_length=20,
            ),
        ),
    ]
