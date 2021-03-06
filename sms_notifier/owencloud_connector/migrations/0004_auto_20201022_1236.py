# Generated by Django 3.1.2 on 2020-10-22 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owencloud_connector', '0003_auto_20201022_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloudevent',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активно'),
        ),
        migrations.AlterField(
            model_name='cloudconnector',
            name='domain',
            field=models.CharField(choices=[('RU', 'RU'), ('UA', 'UA')], default='RU', max_length=2),
        ),
    ]
