# Generated by Django 2.1.5 on 2019-09-20 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recurrence.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('excuse', 'Excuse')], max_length=10)),
                ('registered_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_day', models.DateField(blank=True, null=True)),
                ('level', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1, null=True)),
                ('recurrences', recurrence.fields.RecurrenceField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('capacity', models.IntegerField(blank=True, choices=[(3, 3), (6, 6), (12, 12)], null=True)),
                ('sessions_number', models.IntegerField(blank=True, choices=[(8, 8), (12, 12)], null=True)),
                ('season', models.CharField(blank=True, choices=[('winter', 'Winter'), ('summer', 'Summer')], max_length=200)),
                ('starts_at', models.TimeField(blank=True, null=True)),
                ('ends_at', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('registered_at', models.DateField(auto_now_add=True, null=True)),
                ('reference', models.CharField(blank=True, max_length=5, null=True, unique=True)),
                ('level', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1, null=True)),
                ('club_member', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainees', to='website.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=255)),
                ('reference', models.CharField(blank=True, max_length=5, null=True, unique=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainers', to='website.Trainer'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='website.Class'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='trainee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainees', to='website.Trainee'),
        ),
        migrations.AlterUniqueTogether(
            name='attendancerecord',
            unique_together={('registered_at', 'trainee')},
        ),
    ]
