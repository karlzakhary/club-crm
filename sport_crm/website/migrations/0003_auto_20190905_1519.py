# Generated by Django 2.2.4 on 2019-09-05 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20190905_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainee',
            name='date_of',
        ),
        migrations.AddField(
            model_name='trainee',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='level',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='level',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1, null=True),
        ),
    ]