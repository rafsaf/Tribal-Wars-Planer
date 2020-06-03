from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
"""DATA MODELS"""


class World(models.Model):
    title = models.TextField(verbose_name='Tytuł')
    world = models.IntegerField(verbose_name='Numer świata')

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-world', )


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
            raise ValueError(
                "Unallowed ', ' in Tribe's tag - id:{}, name:{}, please remove it"
                .format(self.tribe_id, self.name))
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


# PLANER MODELS


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
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=8,
                              default='active')
    moje_plemie_skrot = models.CharField(max_length=100,
                                         default='',
                                         null=True,
                                         blank=True)
    przeciwne_plemie_skrot = models.CharField(max_length=100,
                                              default='',
                                              null=True,
                                              blank=True)

    zbiorka_wojsko = models.TextField(
        null=True,
        blank=True,
        default="",
        help_text=mark_safe(
            "Wymagana dokładna forma ze skryptu Wojska, zajrzyj do <a href='/dokumentacja'>dokumentacji</a>"
        ))
    zbiorka_obrona = models.TextField(
        null=True,
        blank=True,
        default="",
        help_text=mark_safe(
            "Wymagana dokładna forma ze skryptu Obrona, zajrzyj do <a href='/dokumentacja'>dokumentacji</a>"
        ))

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'ID:' + str(self.id) + ", Nazwa: " + str(self.nazwa)

    def save(self, *args, **kwargs):
        """
        We need to check zbiorka_wojsko and obrona_wojsko before we can allow user to save it
        \ r \ n spliting!
        """
        if self.zbiorka_wojsko == '':
            pass
        else:
            new = ""
            for i in self.zbiorka_wojsko.split("\r\n"):

                if i == "":
                    continue

                if len(i.split(",")) == 17:
                    if new == "":
                        new = i
                    else:
                        new += "\r\n" + i
                elif len(i.split(",")) == 16:
                    if new == "":
                        new = i + "?,"
                    else:
                        new += "\r\n" + i + "?,"
                else:
                    raise ValueError("Wojska- Błąd w lini: \n{}".format(i))
                self.zbiorka_wojsko = new
        if self.zbiorka_obrona == '':
            pass
        else:
            new = ""
            for i in self.zbiorka_obrona.split("\r\n"):

                if i == "":
                    continue

                elif len(i.split(",")) == 14:
                    if new == "":
                        new = i
                    else:
                        new += "\r\n" + i

                else:
                    raise ValueError("Obrona- Błąd w lini: \n{}".format(i))
                self.zbiorka_obrona = new

        super(New_Outline, self).save(*args, **kwargs)  # Call the real save() method



