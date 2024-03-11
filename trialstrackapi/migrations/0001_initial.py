# Generated by Django 4.1.3 on 2024-03-05 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=50)),
                ('zip', models.IntegerField()),
                ('country', models.CharField(max_length=50)),
                ('geo_lat', models.CharField(max_length=100)),
                ('geo_lon', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=50)),
                ('dob', models.DateField()),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='PatientTrialLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_trial_locations', to='trialstrackapi.patient')),
            ],
            options={
                'db_table': 'patient_trial_location',
            },
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nct_id', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('brief_title', models.TextField()),
                ('study_type', models.CharField(max_length=50)),
                ('overall_status', models.CharField(max_length=50)),
                ('brief_summary', models.TextField()),
                ('detail_description', models.TextField()),
                ('phase', models.CharField(max_length=50)),
                ('eligibility', models.TextField()),
                ('study_first_submit_date', models.DateField()),
                ('last_update_submit_date', models.DateField()),
                ('lead_sponsor_name', models.CharField(max_length=150)),
                ('imported_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'trial',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='TrialLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=100)),
                ('contact_phone', models.CharField(max_length=50)),
                ('contact_email', models.CharField(max_length=100)),
                ('pi_name', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_trials', to='trialstrackapi.location')),
                ('trial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trial_locations', to='trialstrackapi.trial')),
            ],
            options={
                'db_table': 'trial_location',
            },
        ),
        migrations.AddField(
            model_name='trial',
            name='locations',
            field=models.ManyToManyField(related_name='trials', through='trialstrackapi.TrialLocation', to='trialstrackapi.location'),
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_researchers', to='trialstrackapi.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='researcher', to='trialstrackapi.user')),
            ],
            options={
                'db_table': 'researcher',
            },
        ),
        migrations.CreateModel(
            name='PatientTrialLocationCommunication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField()),
                ('patient_trial_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trial_location_researchers', to='trialstrackapi.patienttriallocation')),
            ],
            options={
                'db_table': 'patient_trial_location_communication',
            },
        ),
        migrations.AddField(
            model_name='patienttriallocation',
            name='researcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='researcher_patient_trial_locations', to='trialstrackapi.researcher'),
        ),
        migrations.AddField(
            model_name='patienttriallocation',
            name='trial_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trial_location_patients', to='trialstrackapi.triallocation'),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='trialstrackapi.user'),
        ),
    ]
