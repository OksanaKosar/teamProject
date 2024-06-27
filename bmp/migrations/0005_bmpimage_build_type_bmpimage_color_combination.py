# Generated by Django 4.2.13 on 2024-05-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmp', '0004_alter_bmpimage_image_alter_bmpimage_res_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='bmpimage',
            name='build_type',
            field=models.CharField(choices=[('type1', 'Type 1'), ('type2', 'Type 2'), ('type3', 'Type 3')], default='type1', max_length=50),
        ),
        migrations.AddField(
            model_name='bmpimage',
            name='color_combination',
            field=models.CharField(choices=[('combination1', 'Combination 1'), ('combination2', 'Combination 2'), ('combination3', 'Combination 3')], default='combination1', max_length=50),
        ),
    ]
