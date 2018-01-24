from django.contrib import admin

from app.models import Produit, Categorie, ProduitCategorie, Personne

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(ProduitCategorie)
admin.site.register(Personne)
