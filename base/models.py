from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
# Create your models here.


"""DATA MODELS"""

class World(models.Model):
    title = models.TextField(verbose_name='Tytuł')
    world = models.IntegerField(verbose_name='Numer świata')

    def __str__(self):
        return str(self.title)
    class Meta:
        ordering = ('-world',)

class Tribe(models.Model):
    tribe_id = models.IntegerField()
    name = models.TextField()
    tag = models.TextField()
    members = models.IntegerField()
    villages = models.IntegerField()
    points = models.IntegerField()
    all_points = models.IntegerField()
    rank = models.IntegerField()
    world = models.IntegerField()

    def save(self, *args, **kwargs):
        if ', ' in self.tag:
            raise ValueError("Unallowed ', ' in Tribe's tag - id:{}, name:{}, please remove it".format(self.tribe_id, self.name))
        super().save(*args, **kwargs)


class Player(models.Model):
    player_id = models.IntegerField()
    name = models.TextField()
    tribe_id = models.IntegerField()
    villages = models.IntegerField()
    points = models.IntegerField()
    rank = models.IntegerField()
    world = models.IntegerField()

class Village(models.Model):
    village_id = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    player_id = models.IntegerField()
    world = models.IntegerField()
    points = models.IntegerField(null=True)

"""PLANER MODELS"""

class New_Outline(models.Model):
    worlds = World.objects.all()


    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]


    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    """
    ONLY Chosen in form
    """
    data_akcji = models.DateField(null=True, blank=True)
    nazwa = models.TextField()
    swiat = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default='active')
    moje_plemie_skrot = models.CharField(max_length=100, default='', null=True, blank=True)
    przeciwne_plemie_skrot = models.CharField(max_length=100, default='', null=True, blank=True)

    zbiorka_wojsko = models.TextField(null=True, default="", help_text=mark_safe(
        "Wymagana dokładna forma ze skryptu Wojska, zajrzyj do <a href='/dokumentacja'>dokumentacji</a>"))
    zbiorka_obrona = models.TextField(null=True, default="", help_text=mark_safe(
        "Wymagana dokładna forma ze skryptu Obrona, zajrzyj do <a href='/dokumentacja'>dokumentacji</a>"))

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'ID:'+ str(self.id) + ", Nazwa: " + str(self.nazwa)
