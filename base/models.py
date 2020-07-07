from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField

# DATA MODELS


class World(models.Model):
    """
    class representing village in game
     \n Member variables:
     \n title -str
     \n world- int
     \n speed_world -float
     \n speed_units -float
     \n paladin - active/inactive
     \n archer - active/inactive
     \n militia - active/inactive
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    # Kiedys dodac test czy istnieja pliki txt w api gry o numerze
    title = models.TextField(verbose_name="Tytuł")
    world = models.IntegerField(verbose_name="Numer świata")
    speed_world = models.FloatField(null=True, blank=True, default=1)
    speed_units = models.FloatField(null=True, blank=True, default=1)

    # Some units are not aviable on worlds!!!
    paladin = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    archer = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    militia = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title != "Świat {}".format(self.world):
            raise Exception("Invalid World title: {}".format(self.title))
        super(World, self).save(*args, **kwargs)  # Call the real save() method

    class Meta:
        ordering = ("-world",)


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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if ", " in self.tag:
            raise ValueError(
                "Unallowed ', ' in Tribe's tag - id:{}, name:{}, please remove it".format(
                    self.tribe_id, self.name
                )
            )
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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return str(self.village_id)


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
     \n initial_period_outline_players -str NULL BLANK DEFAULT ""
     \n initial_period_outline_targets -str NULL BLANK DEFAULT ""
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # ONLY Chosen in form
    data_akcji = models.DateField(null=True, blank=True)
    nazwa = models.TextField()
    swiat = models.TextField(null=True, blank=True)
    #
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    moje_plemie_skrot = models.CharField(max_length=100, default="", blank=True)
    przeciwne_plemie_skrot = models.CharField(max_length=100, default="", blank=True)

    zbiorka_wojsko = models.TextField(
        null=True,
        blank=True,
        default="",
        help_text=mark_safe(
            "Wymagana dokładna forma ze skryptu Wojska, zajrzyj do <a href='/documentation#Skrypt-zbiorka-wojska'>dokumentacji</a>"
        ),
    )
    zbiorka_obrona = models.TextField(
        null=True,
        blank=True,
        default="",
        help_text=mark_safe(
            "Wymagana dokładna forma ze skryptu Obrona, zajrzyj do <a href='/documentation#Skrypt-zbiorka-obrona'>dokumentacji</a>"
        ),
    )

    initial_period_outline_players = models.TextField(blank=True, default="")

    initial_period_outline_targets = models.TextField(blank=True, default="")

    max_distance_initial_outline = models.IntegerField(blank=True, default=10)

    
    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "ID:" + str(self.id) + ", Nazwa: " + str(self.nazwa)


class Results(models.Model):
    """ One to one with outline, presents results """

    outline = models.OneToOneField(
        New_Outline, on_delete=models.CASCADE, primary_key=True
    )
    results_get_deff = models.TextField(default="")

    def __str__(self):
        return self.outline.nazwa + " results"


class Documentation(models.Model):
    title = models.CharField(max_length=10)
    main_page = MarkdownxField()

    def __str__(self):
        return self.title

class Target_Vertex(models.Model):
    outline = models.ForeignKey(New_Outline, on_delete=models.CASCADE)
    target = models.CharField(max_length=7, null=True)
    attack1 = models.CharField(max_length=7, null=True)
    attack2 = models.CharField(max_length=7, null=True)
    attack3 = models.CharField(max_length=7, null=True)
    attack4 = models.CharField(max_length=7, null=True)
    attack5 = models.CharField(max_length=7, null=True)
    attack6 = models.CharField(max_length=7, null=True)
    attack7 = models.CharField(max_length=7, null=True)
    attack8 = models.CharField(max_length=7, null=True)
    attack9 = models.CharField(max_length=7, null=True)
    attack10 = models.CharField(max_length=7, null=True)

    def set_next(self, coords):
        for i in [a for a in dir(self) if not a.startswith('__') and a.startswith("attack")]:
            dict_ = self.__dict__
            if dict_[i] == None:
                dict_[i]=coords
                return