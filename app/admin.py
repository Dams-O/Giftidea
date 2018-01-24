from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from app.models import Produit, Categorie, ProduitCategorie, Personne, Picture


class PictureAdmin(admin.ModelAdmin):
    def list_url_image(self, obj):
        if obj and obj.fichier:
            u, ut = obj.url_fichier(), obj.url_fichier()
            return '<a target="_blank" href="{}">' \
                   '<img src="{}" alt="{}" title="" ' \
                   'style="width: auto; height: 50px; max-height:50px" />' \
                   '</a>'.format(u, ut, ut, ut)
        return None
    list_url_image.short_description = _('Image')
    list_url_image.allow_tags = True

    list_display = ('produit', 'list_url_image')
    list_display_links = ('list_url_image', )
    readonly_fields = ('list_url_image',)

    fieldsets = (
        (None, {
            'fields': (('produit',), ('fichier',))
        }),
    )


admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(ProduitCategorie)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Personne)
