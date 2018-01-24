import random
import uuid

import os
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags import staticfiles
from django.db import models
from django.urls import reverse_lazy
from os.path import splitext, basename
from django.utils.datetime_safe import datetime as datetime_safe

from giftideas import settings


class Movie(models.Model):
    actors = models.ManyToManyField(
        'Personne',
        blank=True, null=True,
        related_name='films',
        through='MoviePersonne'
    )


class MoviePersonne(models.Model):
    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE)
    personne = models.ForeignKey('Personne',
                                 on_delete=models.CASCADE)
    paie = models.BigIntegerField(default=0)


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


class Picture(models.Model):

    upload_directory = os.path.join(settings.MEDIA_ROOT, 'photos')
    # Générer un nom de fichier dynamiquement :

    def generate_filename(self, filename):
        # nom: "bea536a0-089c-a45b.pdf"
        nom = UidMixin.generate_uid(splitext(basename(filename))[1])
        # Retour ex: "profiles/bea536a0/089c/a45b.pdf"
        return os.path.join(self.upload_directory, nom)

    produit = models.ForeignKey(Produit,
                                default=None, blank=True,
                                null=True,
                                on_delete=models.CASCADE)
    fichier = models.FileField(
        default=None, null=True, blank=True,
        upload_to=generate_filename,)

    def url_fichier(self, default=None):
        if self.fichier is None:
            if default:
                return staticfiles.static(default)
            return staticfiles.static('img/no-image-yet.jpg')
        nom = self.fichier.name
        if nom.startswith('./'):
            nom = nom[2:]
        found = nom.find(settings.MEDIA_ROOT)
        if found >= 0:
            nom = nom[found + 1 + len(settings.MEDIA_ROOT):]
        return str(reverse_lazy('url_public', args=(nom,)))


class ProduitCategorie(models.Model):
    categorie = models.ForeignKey(Categorie,
                                  on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,
                                on_delete=models.CASCADE)


class UidMixin(object):
    @staticmethod
    def generate_uid(text_to_append='', salt=''):
        # pris ici : http://stackoverflow.com/questions/
        # 6999726/how-can-i-convert-a-datetime-object-to
        # -milliseconds-since-epoch-unix-time-in-p
        #
        epoch = datetime_safe.utcfromtimestamp(0)

        def millis(dt):
            return (dt - epoch).total_seconds() * 1000.0

        nom = str(random.randint(0, 90000000) +
                  int(millis(datetime_safe.now())))
        return str(uuid.uuid5(uuid.NAMESPACE_OID, nom + salt)) + text_to_append


class Personne(models.Model):
    user = models.OneToOneField(User)
    cadeaux = models.ManyToManyField(
        Produit,
        blank=True,
        default=None,
        related_name='participants')

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
