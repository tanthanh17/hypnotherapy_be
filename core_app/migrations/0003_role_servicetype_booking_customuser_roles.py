# Generated by Django 4.2.16 on 2024-11-30 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0002_alter_customuser_options_alter_customuser_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'service_type',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_name', models.CharField(max_length=255)),
                ('booking_id', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('completed', 'Completed'), ('unpaid', 'Unpaid'), ('pending', 'Pending')], default='unpaid', max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('duration', models.PositiveIntegerField()),
                ('service_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core_app.servicetype')),
            ],
            options={
                'db_table': 'booking',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='roles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core_app.role'),
        ),
    ]