# Generated by Django 5.1.5 on 2025-02-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0006_user_is_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponQuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_quota', models.PositiveIntegerField(default=5)),
            ],
        ),
    ]
