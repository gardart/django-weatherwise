from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weatherwane", "0002_remove_station_auto_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="station",
            name="name",
            field=models.CharField(
                default="",
                help_text="Required station name (e.g., Keflavik Airport)",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="station",
            name="code",
            field=models.CharField(
                default="",
                help_text="Required station code from the XML feed (e.g., 0401)",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="station",
            name="source",
            field=models.CharField(
                blank=True,
                help_text="Optional source/provider note (e.g., Icelandic Met Office)",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="station",
            name="latitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                help_text="Latitude in decimal degrees (e.g., 63.962800)",
                max_digits=11,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="station",
            name="longitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                help_text="Longitude in decimal degrees (e.g., -20.566900)",
                max_digits=11,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="station",
            name="elevation",
            field=models.IntegerField(
                blank=True,
                help_text="Elevation in meters above sea level (e.g., 52)",
                null=True,
            ),
        ),
    ]
