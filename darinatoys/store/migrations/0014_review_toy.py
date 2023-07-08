# Generated by Django 4.2.1 on 2023-07-06 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_review_toy_toy_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='toy',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='store.toy', verbose_name='Связь к игрушке'),
            preserve_default=False,
        ),
    ]
