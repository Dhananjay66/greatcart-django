# Generated by Django 5.2 on 2025-05-07 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_product_decsription_product_decsription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='decsription',
            new_name='description',
        ),
    ]
