from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Station",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                ("code", models.CharField(max_length=20)),
                ("source", models.CharField(blank=True, max_length=200, null=True)),
                ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True)),
                ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True)),
                ("elevation", models.IntegerField(blank=True, null=True)),
                ("auto_update", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["code"],
            },
        ),
        migrations.CreateModel(
            name="Observation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data", models.TextField(blank=True, null=True)),
                ("observation_type", models.CharField(blank=True, max_length=5, null=True)),
                ("observation_cycle", models.IntegerField(blank=True, null=True)),
                ("observation_time", models.DateTimeField(blank=True, null=True)),
                ("wind_compass", models.CharField(blank=True, max_length=4, null=True, verbose_name="WC")),
                ("wind_speed", models.IntegerField(blank=True, null=True, verbose_name="WS")),
                ("wind_speed_gust", models.IntegerField(blank=True, null=True, verbose_name="WSG")),
                ("wind_speed_max", models.IntegerField(blank=True, null=True, verbose_name="WSM")),
                ("visibility", models.CharField(blank=True, max_length=5, null=True, verbose_name="VIS")),
                ("temperature", models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name="T")),
                ("dewpoint", models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name="DEW")),
                ("sky_conditions", models.TextField(blank=True, null=True, verbose_name="SKY")),
                ("cloud_cover", models.IntegerField(blank=True, null=True, verbose_name="CLC")),
                ("weather_conditions", models.TextField(blank=True, null=True, verbose_name="CON")),
                ("sealevel_pressure", models.IntegerField(blank=True, null=True, verbose_name="P")),
                ("relative_humidity", models.IntegerField(blank=True, null=True, verbose_name="RH")),
                ("precipitation", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="PRE")),
                ("snc", models.TextField(blank=True, null=True)),
                ("snd", models.IntegerField(blank=True, null=True)),
                ("sed", models.TextField(blank=True, null=True)),
                ("station", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="weatherwane.station")),
            ],
            options={
                "ordering": ["-observation_time"],
            },
        ),
    ]
