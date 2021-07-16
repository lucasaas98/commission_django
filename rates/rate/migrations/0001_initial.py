# Generated by Django 3.1.7 on 2021-07-16 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=200)),
                ('rate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation', models.CharField(max_length=200)),
                ('checkin_date', models.DateTimeField()),
                ('flat', models.CharField(max_length=200)),
                ('income', models.FloatField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rate.city')),
            ],
        ),
    ]
