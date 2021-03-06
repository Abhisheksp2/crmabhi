# Generated by Django 3.0 on 2020-09-02 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200901_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customar',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='accounts.Customer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
