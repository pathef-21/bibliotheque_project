from django.db import models
from django.contrib.auth.models import User

class Auteur(models.Model):
    """
    Représente un auteur de livres.
    Django crée automatiquement un champ 'id' (clé primaire).
    """

    # CharField : texte de longueur limitée (obligatoire)
    nom = models.CharField(
        max_length=200,
        verbose_name='Nom complet'
    )

    # TextField : texte long (optionnel avec blank=True, null=True)
    biographie = models.TextField(
        blank=True,        # Formulaires : champ non obligatoire
        null=True,         # Base de données : colonne peut être NULL
        verbose_name='Biographie'
    )

    # CharField optionnel
    nationalite = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Nationalité'
    )

    # DateField : date (auto_now_add = rempli automatiquement à la création)
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    def __str__(self):
        # Représentation lisible dans l'admin et le shell
        return self.nom

    class Meta:
        # Ordre par défaut des requêtes
        ordering = ['nom']
        verbose_name = 'Auteur'
        verbose_name_plural = 'Auteurs'


class Livre(models.Model):
    """
    Représente un livre.
    Chaque livre a UN auteur (ForeignKey = N vers 1).
    Un auteur peut avoir PLUSIEURS livres.
    """

    # Choix prédéfinis pour le champ categorie
    CATEGORIES = [
        ('roman', 'Roman'),
        ('essai', 'Essai'),
        ('poesie', 'Poésie'),
        ('bd', 'Bande dessinée'),
        ('science', 'Science'),
        ('histoire', 'Histoire'),
    ]

    titre = models.CharField(max_length=300, verbose_name='Titre')

    # CharField avec unique=True : valeur unique dans toute la table
    isbn = models.CharField(
        max_length=17,
        unique=True,
        verbose_name='ISBN'
    )

    # IntegerField avec validation de plage
    annee_publication = models.IntegerField(
        verbose_name='Année de publication'
    )

    # Choix avec valeur par défaut
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='roman',
        verbose_name='Catégorie'
    )

    # ForeignKey : relation N livres → 1 auteur
    # on_delete=CASCADE : si l'auteur est supprimé, ses livres aussi
    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.CASCADE,
        related_name='livres',   # auteur.livres.all() retourne ses livres
        verbose_name='Auteur'
    )

    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titre} ({self.annee_publication})'

    class Meta:
        ordering = ['-annee_publication', 'titre']

class Emprunt(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    livre = models.ForeignKey('Livre', on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour_prevue = models.DateField()
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur} - {self.livre}"
