# Generated by Django 2.0.2 on 2018-03-14 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('basic_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('bonus', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('allowances', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('deductions', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('gross_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('ssf_employee', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('ssf_employer', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('taxable_income', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('paye', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('net_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_payroll', related_query_name='created_payrolls', to=settings.AUTH_USER_MODEL)),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_payroll', related_query_name='created_payrolls', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employers.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
