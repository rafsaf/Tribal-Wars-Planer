from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
# DATA MODELS


class World(models.Model):
    """
    class representing village in game
     \n Member variables:
     \n title -str
     \n world- int
     \n speed_world -float
     \n speed_units -float
    """
    # Kiedys dodac test czy istnieja pliki txt w api gry o numerze
    title = models.TextField(verbose_name='Tytuł')
    world = models.IntegerField(verbose_name='Numer świata')
    speed_world = models.FloatField(null=True, blank=True, default=1)
    speed_units = models.FloatField(null=True, blank=True, default=1)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title != 'Świat {}'.format(self.world):
            raise Exception("Invalid World title: {}".format(self.title))
        super(World, self).save(*args, **kwargs)  # Call the real save() method

    class Meta:
        ordering = ('-world', )



class Tribe(models.Model):
    """
    class representing tribe in game
     \n Member variables:
     \n tribe_id -int
     \n name -str
     \n tag -str
     \n members -int
     \n villages -int
     \n points -int
     \n all_points -int
     \n rank -int
     \n world -int
    """
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
    """
    class representing player in game
     \n Member variables:
     \n player_id -int
     \n name -str
     \n tribe_id -int
     \n villages -int
     \n points -int
     \n rank -int
     \n world -int
    """
    player_id = models.IntegerField()
    name = models.TextField()
    tribe_id = models.IntegerField()
    villages = models.IntegerField()
    points = models.IntegerField()
    rank = models.IntegerField()
    world = models.IntegerField()


class Village(models.Model):
    """
    class representing village in game
     \n Member variables:
     \n village_id -int
     \n x -int
     \n y -int
     \n player_id -int
     \n world -int
     \n points -int
    """
    village_id = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    player_id = models.IntegerField()
    world = models.IntegerField()
    points = models.IntegerField(null=True)


# PLANER MODELS


class New_Outline(models.Model):
    """
     \n owner USER instance
     \n data_akcji - date_field
     \n nazwa -str
     \n swiat -str NULL, BLANK
     \n created -date_time AUTO_NOW_ADD
     \n status -str: DEFAULT 'active'
     \n moje_plemie_skrot -str: pl1, pl2, pl3, ... NULL BLANK DEFAULT ""
     \n przeciwne_plemie_skrot -str: pl1, pl2, pl3, ... NULL BLANK DEFAULT ""
     \n zbiorka_wojsko -str NULL BLANK DEFAULT ""
     \n zbiorka_obrona -str NULL BLANK DEFAULT ""
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # ONLY Chosen in form
    data_akcji = models.DateField(null=True, blank=True)
    nazwa = models.TextField()
    swiat = models.TextField(null=True, blank=True)
    #
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

                if len(i.split(",")) == 14:
                    if new == "":
                        new = i
                    else:
                        new += "\r\n" + i

                else:
                    raise ValueError("Obrona- Błąd w lini: \n{}".format(i))
            self.zbiorka_obrona = new
        super().save(*args, **kwargs)  # Call the real save() method

