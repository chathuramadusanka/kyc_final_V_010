# Generated by Django 2.2.10 on 2021-05-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0023_auto_20210506_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='id_info',
            name='city_ref',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='id_info',
            name='house_num',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='id_info',
            name='name_full',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='id_info',
            name='street_add',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='city_per_temp',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='city_temp',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='email_add_temp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='house_no_per_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='house_no_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='state_address_temp',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='street_per_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_info',
            name='street_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='city_per_temp',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='city_temp',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='email_add_temp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='house_no_per_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='house_no_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='state_address_temp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='street_per_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_infotemp',
            name='street_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='city_per_temp',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='city_temp',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='date_now_temp',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='email_add_temp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='file_note_temp',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='house_no_per_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='house_no_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='reason_for_rej_temp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='rejected_temp',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='state_address_temp',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='street_per_temp',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='kyc_reject',
            name='street_temp',
            field=models.CharField(max_length=100),
        ),
    ]