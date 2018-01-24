from django.contrib.auth.models import User
from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=200,
                           default=None,
                           blank=True,
                           help_text='La catégorie')


class Produit(models.Model):
    nom = models.CharField(max_length=200,
                           default=None,
                           blank=True,
                           help_text='Le cadeau')
    detail = models.TextField(default=None,
                              blank=True,
                              null=True)
    prix = models.FloatField(default=0.0, blank=True)
    votes = models.ManyToManyField('Personne',
                                   blank=True,
                                   default=None)
    categories = models.ManyToManyField(
        Categorie, blank=True, default=None,
        through='ProduitCategorie')

    def __str__(self):
        return '{} ({})'.format(self.nom, self.prix)


class ProduitCategorie(models.Model):
    categorie = models.ForeignKey(Categorie,
                                  on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,
                                on_delete=models.CASCADE)


class Personne(models.Model):
    user = models.OneToOneField(User)
    cadeaux = models.ManyToManyField(Produit,
                                     blank=True,
                                     default=None)

    def description(self):
        retour = '{} {}'.format(
            self.user.first_name if self.user.first_name else '',
            self.user.last_name if self.user.last_name else '',
        ).strip()
        if retour == '':
            retour = self.user.username
        return retour.capitalize()

    def __str__(self):
        return self.description()

    contributions = models.ManyToManyField(
        Produit,
        blank=True,
        default=None,
        related_name='contributions')
