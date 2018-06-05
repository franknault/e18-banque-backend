# Generated by Django 2.0.5 on 2018-06-05 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('no_civique', models.CharField(max_length=30)),
                ('nom_rue', models.CharField(max_length=50)),
                ('code_postal', models.CharField(max_length=6)),
                ('ville', models.CharField(max_length=100)),
                ('pays', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'adresse',
                'verbose_name_plural': 'adresses',
                'db_table': 'adresse',
            },
        ),
        migrations.CreateModel(
            name='CarteCredit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom_titulaire', models.CharField(max_length=200)),
                ('num_carte', models.CharField(max_length=100, unique=True)),
                ('annee_expiration', models.CharField(max_length=2)),
                ('mois_expiration', models.CharField(max_length=2)),
                ('cvv', models.CharField(max_length=255)),
                ('date_emission', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'cartecredit',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('telephone', models.CharField(max_length=11)),
                ('type', models.CharField(choices=[('E', 'Entreprise'), ('P', 'Particulier')], max_length=1)),
                ('nom_particulier', models.CharField(blank=True, max_length=50, null=True)),
                ('prenom_particulier', models.CharField(blank=True, max_length=50, null=True)),
                ('sexe', models.CharField(blank=True, choices=[('H', 'Homme'), ('F', 'Femme'), ('A', 'Non défini')], max_length=1, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('nom_entreprise', models.CharField(blank=True, max_length=50, null=True)),
                ('numero_entreprise', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num_compte', models.CharField(max_length=8, unique=True)),
                ('solde', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_ouverture', models.DateTimeField(auto_now_add=True)),
                ('date_fermeture', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'compte',
            },
        ),
        migrations.CreateModel(
            name='InfoAuthentification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom_usager', models.CharField(max_length=20, unique=True)),
                ('mdp', models.CharField(max_length=512)),
                ('courriel', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, max_length=512, null=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_debut', models.DateTimeField(auto_now_add=True)),
                ('date_fin', models.DateTimeField(null=True)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('solde_avant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('solde_apres', models.DecimalField(decimal_places=2, max_digits=10)),
                ('etat', models.CharField(choices=[('ACC', 'Acceptée'), ('REF', 'Refusée'), ('GEL', 'Gelée')], max_length=3)),
            ],
            options={
                'db_table': 'transaction',
            },
        ),
        migrations.CreateModel(
            name='TypeTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('VMT', 'Virement debit-debit'), ('PMT', 'Paiement debit-credit'), ('ACT', 'Achat debit-credit'), ('RBT', 'Remboursement credit-credit')], max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'type_transaction',
            },
        ),
        migrations.CreateModel(
            name='Courant',
            fields=[
                ('compte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='api.Compte')),
                ('courant_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'courant',
            },
            bases=('api.compte',),
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('compte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='api.Compte')),
                ('credit_id', models.AutoField(primary_key=True, serialize=False)),
                ('limite', models.DecimalField(decimal_places=2, max_digits=10)),
                ('carte_credit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.CarteCredit')),
            ],
            options={
                'db_table': 'credit',
            },
            bases=('api.compte',),
        ),
        migrations.AddField(
            model_name='transaction',
            name='compte',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Compte'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type_transaction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Transaction'),
        ),
        migrations.AddField(
            model_name='client',
            name='info_authentification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.InfoAuthentification'),
        ),
        migrations.AddField(
            model_name='adresse',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Client'),
        ),
        migrations.AddField(
            model_name='administrateur',
            name='info_authentification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.InfoAuthentification'),
        ),
        migrations.AddField(
            model_name='credit',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Client'),
        ),
        migrations.AddField(
            model_name='courant',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Client'),
        ),
    ]
