# Generated by Django 3.1.7 on 2021-04-27 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0008_auto_20210427_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='profile_pic_temp',
            field=models.FileField(null=True, upload_to='images/', verbose_name=''),
        ),
    ]