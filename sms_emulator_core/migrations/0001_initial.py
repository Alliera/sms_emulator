# Generated by Django 3.1.4 on 2020-12-22 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('webhook_url', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Enterprise',
                'verbose_name_plural': 'Enterprises',
                'db_table': 'enterprise',
            },
        ),
        migrations.CreateModel(
            name='SMSMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_sender', models.CharField(max_length=255)),
                ('to_receiver', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
                ('direction', models.CharField(choices=[('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')], max_length=255)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sms_messages', to='sms_emulator_core.enterprise')),
            ],
            options={
                'verbose_name': 'SMS Message',
                'verbose_name_plural': 'SMS Messages',
                'db_table': 'sms_message',
            },
        ),
    ]
