# Generated by Django 2.0.2 on 2018-03-07 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import employers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('postal_address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('regular', 'Regular')], default='regular', max_length=10)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=employers.models.admin_avatar_location)),
                ('user_type', models.CharField(default='employer', max_length=10)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_administrator', related_query_name='created_administrators', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_administrator', related_query_name='created_administrators', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_department', related_query_name='created_departments', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_department', related_query_name='created_departments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('headshot', models.ImageField(blank=True, null=True, upload_to=employers.models.headshot_location)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('marital_status', models.CharField(blank=True, choices=[('married', 'Married'), ('single', 'Single'), ('engaged', 'Engaged'), ('divorced', 'Divorced')], max_length=10, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employers.Address')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_employee', related_query_name='created_employees', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_employee', related_query_name='created_employees', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=employers.models.logo_location)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employers.Address')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_employer', related_query_name='created_employers', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_employer', related_query_name='created_employers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employers.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('allowances', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('deductions', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employers.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_salary', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('employee_no', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('date_of_employment', models.DateField(blank=True, null=True)),
                ('social_security_no', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employers.Department')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employers.Employee')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employers.JobTitle')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employers.Employer'),
        ),
        migrations.AddField(
            model_name='department',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employers.Employer'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employers.Employer'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
