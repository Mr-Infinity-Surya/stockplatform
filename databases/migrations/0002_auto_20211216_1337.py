# Generated by Django 3.2.9 on 2021-12-16 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='Stock_ISIN',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='databases.stock'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='Stock_ISIN',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='databases.stock'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ISIN',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False),
        ),
    ]