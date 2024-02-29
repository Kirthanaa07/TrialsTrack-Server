# Generated by Django 4.1.3 on 2024-02-29 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trialstrackapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientClinicalTrialLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('clinical_trial_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trialstrackapi.clinicaltriallocation')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trialstrackapi.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ClinicalTrialLocationResearcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinical_trial_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trialstrackapi.clinicaltriallocation')),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trialstrackapi.researcher')),
            ],
        ),
    ]
