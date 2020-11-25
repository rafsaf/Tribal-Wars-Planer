from django.db.models import F, DecimalField, ExpressionWrapper, Max

from base import models
from tribal_wars import basic

class WriteTarget:
    def __init__(self, target: models.TargetVertex, outline: models.Outline):
        self.target = target
        self.x_coord = target.coord_tuple()[0]
        self.y_coord = target.coord_tuple()[1]
        self.outline = outline
        self.mode_off = target.mode_off
        self.mode_noble = target.mode_noble
        self.mode_division = target.mode_division

    def sorted_weights(self):
        default_off_query = models.WeightMaximum.objects.filter(outline=self.outline, off_max__gte=self.outline.initial_outline_min_off).annotate(distance=ExpressionWrapper(((F('x_coord') - self.x_coord) ** 2 + (F('y_coord') - self.y_coord) ** 2) ** (1/2), output_field=DecimalField(max_digits=2)))
        
        

