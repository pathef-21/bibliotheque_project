from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Auteur, Livre

# Personnalisation du titre
admin.site.site_header = "◈ BIBLIOTHÈQUE API"
admin.site.site_title = "Admin"
admin.site.index_title = "Tableau de bord"


class FuturisticAdmin(admin.ModelAdmin):
    """Classe de base qui injecte le CSS futuriste"""
    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }


@admin.register(Auteur)
class AuteurAdmin(FuturisticAdmin):
    list_display = ['nom', 'nationalite', 'date_creation']
    search_fields = ['nom', 'nationalite']


@admin.register(Livre)
class LivreAdmin(FuturisticAdmin):
    list_display = ['titre', 'auteur', 'annee_publication', 'categorie', 'disponible']
    list_filter = ['categorie', 'disponible']
    search_fields = ['titre', 'isbn']