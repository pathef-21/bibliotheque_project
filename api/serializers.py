# api/serializers.py

from rest_framework import serializers
from .models import Auteur, Livre


# ────────────────────────────────
# 1. Serializer simple (manuel)
# ────────────────────────────────
class AuteurSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # ID non modifiable
    nom = serializers.CharField(max_length=200)    # Nom obligatoire
    nationalite = serializers.CharField(max_length=100, required=False)  # Optionnel

    def create(self, validated_data):
        """Création d'un nouvel auteur"""
        return Auteur.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Mise à jour d'un auteur existant"""
        instance.nom = validated_data.get('nom', instance.nom)
        instance.nationalite = validated_data.get('nationalite', instance.nationalite)
        instance.save()
        return instance


# ────────────────────────────────
# 2. ModelSerializer (recommandé)
# ────────────────────────────────
class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur                  # Modèle lié
        fields = '__all__'              # Tous les champs
        read_only_fields = ['id']       # Champs non modifiables


# ────────────────────────────────
# 3. Serializer avec validation
# ────────────────────────────────
class LivreSerializer(serializers.ModelSerializer):

    # Champ calculé (non stocké en base)
    auteur_nom = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_nom', 'disponible'
        ]
        read_only_fields = ['id']

    def get_auteur_nom(self, obj):
        """Retourne le nom de l'auteur"""
        return obj.auteur.nom

    def validate_isbn(self, value):
        """Validation de l'ISBN (13 chiffres)"""
        clean = value.replace('-', '')
        if not clean.isdigit() or len(clean) != 13:
            raise serializers.ValidationError(
                "L'ISBN doit contenir exactement 13 chiffres."
            )
        return value

    def validate_annee_publication(self, value):
        """Validation de l'année"""
        if value < 1000 or value > 2025:
            raise serializers.ValidationError(
                "L'année doit être entre 1000 et 2025."
            )
        return value

    def validate(self, data):
        """Validation globale (plusieurs champs)"""
        if data.get('categorie') == 'essai':
            auteur = data.get('auteur')
            if auteur and not auteur.biographie:
                raise serializers.ValidationError(
                    "Les essais nécessitent une biographie de l'auteur."
                )
        return data


# ────────────────────────────────
# 4. Serializer imbriqué (nested)
# ────────────────────────────────
class LivreDetailSerializer(serializers.ModelSerializer):

    # Affichage complet de l'auteur (lecture seule)
    auteur = AuteurSerializer(read_only=True)

    # Permet d'envoyer l'ID de l'auteur pour créer/modifier
    auteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Auteur.objects.all(),
        source='auteur',
        write_only=True
    )

    class Meta:
        model = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_id', 'disponible'
        ]