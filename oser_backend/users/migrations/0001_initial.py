# Generated by Django 2.0.2 on 2018-03-01 22:32

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models.users


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('tutoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_of_birth', models.DateField(null=True, verbose_name='date de naissance')),
                ('gender', models.CharField(choices=[('M', 'Homme'), ('F', 'Femme')], default='M', max_length=1, verbose_name='sexe')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='téléphone')),
                ('profile_type', models.CharField(choices=[('student', 'Lycéen'), ('tutor', 'Tuteur'), ('schoolstaffmember', 'Membre du personnel de lycée')], max_length=20, null=True, verbose_name='type de profil')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.users.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile_object', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='utilisateur')),
            ],
            options={
                'verbose_name': 'profil',
                'ordering': ['user__last_name', 'user__first_name'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='SchoolStaffMember',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Profile')),
                ('role', models.CharField(max_length=100, verbose_name='rôle')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffmembers', to='tutoring.School', verbose_name='lycée')),
            ],
            options={
                'verbose_name': 'membre du personnel de lycée',
                'verbose_name_plural': 'membres du personnel de lycée',
            },
            bases=('users.profile',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Profile')),
                ('address', models.CharField(max_length=200, verbose_name='adresse')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='tutoring.School')),
                ('tutoring_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='tutoring.TutoringGroup')),
            ],
            options={
                'verbose_name': 'lycéen',
            },
            bases=('users.profile',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Profile')),
                ('promotion', models.IntegerField(choices=[(2020, '2020'), (2019, '2019'), (2018, '2018'), (2017, '2017'), (2016, '2016'), (2015, '2015'), (2014, '2014'), (2013, '2013'), (2012, '2012'), (2011, '2011')], default=2020)),
            ],
            options={
                'verbose_name': 'tuteur',
            },
            bases=('users.profile',),
        ),
    ]