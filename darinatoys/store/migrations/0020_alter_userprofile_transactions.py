# Generated by Django 4.2.1 on 2023-07-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_userprofile_transactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='transactions',
            field=models.ManyToManyField(blank=True, to='store.transaction', verbose_name='Заказы'),
        ),
    ]
