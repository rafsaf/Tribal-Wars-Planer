""" Database models """

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from markdownx.models import MarkdownxField


class World(models.Model):
    """ World in the game """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    title = models.TextField(verbose_name="Tytuł")
    world = models.IntegerField(verbose_name="Numer świata")
    speed_world = models.FloatField(null=True, blank=True, default=1)
    speed_units = models.FloatField(null=True, blank=True, default=1)
    paladin = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    archer = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    militia = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")

    def __str__(self):
        return str(self.title)

    # pylint: disable=W:279
    def save(self, *args, **kwargs):
        if self.title != "Świat {}".format(self.world):
            raise Exception("Invalid World title: {}".format(self.title))
        super(World, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-world",)


class TribeHasUnallowedPatternInTag(Exception):
    """ Tribe Exception """


class Tribe(models.Model):
    """ Tribe in game """
    id = models.CharField(primary_key=True, max_length=11)
    tribe_id = models.IntegerField()
    tag = models.TextField()
    world = models.IntegerField()

    def __str__(self):
        return self.tag

    # pylint: disable=W:279
    def save(self, *args, **kwargs):
        if ", " in self.tag:
            raise TribeHasUnallowedPatternInTag(
                f"Unallowed ', ' in Tribe's tag - id:{self.tribe_id}, name:{self.tag}"
                f"please remove it"
            )
        super().save(*args, **kwargs)


class Player(models.Model):
    """ Player in the game """
    id = models.CharField(primary_key=True, max_length=30)
    player_id = models.IntegerField()
    name = models.TextField()
    tribe_id = models.IntegerField()
    world = models.IntegerField()

    def __str__(self):
        return self.name


class VillageModel(models.Model):
    """ Village in the game """
    id = models.CharField(primary_key=True, max_length=9)
    village_id = models.IntegerField()
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    player_id = models.IntegerField()
    world = models.IntegerField(db_index=True)


    def __str__(self):
        return str(self.village_id)


class Outline(models.Model):
    """ Outline with all informations about it"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    name = models.TextField()
    world = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    editable = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    ally_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)
    enemy_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)
    initial_outline_players = models.TextField(blank=True, default="")
    initial_outline_targets = models.TextField(blank=True, default="")
    off_troops = models.TextField(
        blank=True,
        default="",
    )
    deff_troops = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "ID:" + str(self.id) + ", Nazwa: " + str(self.name)


class Result(models.Model):
    """ Presents Outline and Deff results """

    outline = models.OneToOneField(Outline, on_delete=models.CASCADE, primary_key=True)
    results_get_deff = models.TextField(default="")

    def __str__(self):
        return self.outline.name + " results"


class Documentation(models.Model):
    """ Docs page """

    title = models.CharField(max_length=10)
    main_page = MarkdownxField()

    def __str__(self):
        return self.title


class TargetVertex(models.Model):
    """ Target Village """

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    target = models.CharField(max_length=7)
    player = models.CharField(max_length=30)

    def __str__(self):
        return self.target

    def get_absolute_url(self):
        return reverse('base:planer_initial_detail', args=[self.outline_id, self.id])


class WeightMaximum(models.Model):
    """ Control state smaller than maximum """

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    start = models.CharField(max_length=7)
    player = models.CharField(max_length=30)
    off_max = models.IntegerField()
    off_state = models.IntegerField(default=0)
    off_left = models.IntegerField()
    nobleman_max = models.IntegerField()
    nobleman_state = models.IntegerField(default=0)
    nobleman_left = models.IntegerField()

    def __str__(self):
        return self.start


class WeightModel(models.Model):
    """ Command between start and target """

    target = models.ForeignKey(TargetVertex, on_delete=models.CASCADE)
    state = models.ForeignKey(WeightMaximum, on_delete=models.CASCADE)
    start = models.CharField(max_length=7)
    off = models.IntegerField()
    distance = models.FloatField()
    nobleman = models.IntegerField()
    order = models.IntegerField()
    player = models.CharField(max_length=40)

    def __str__(self):
        return self.start
