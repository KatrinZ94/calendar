# Generated by Django 3.2.5 on 2021-07-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124, verbose_name='страна')),
            ],
        ),
        migrations.AlterField(
            model_name='userevent',
            name='reminder_before',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'час'), (2, '2 часа'), (4, '4 часа'), (24, 'день'), (168, 'неделю')], help_text='выберите время напоминания', null=True, verbose_name='напоминание о событии'),
        ),
    ]
