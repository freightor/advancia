# Generated by Django 2.0.2 on 2018-03-14 15:20

from django.db import migrations, models
import django.db.models.deletion
import django_otp.util
import otp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TOTPDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
                ('key', models.CharField(default=otp.models.default_key, max_length=60, unique=True, validators=[django_otp.util.hex_validator])),
                ('last_verified_counter', models.BigIntegerField(default=-1)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employers.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
