from django.test import TestCase
from . import models


class TribeTagWithoutUnallowedPatterns(TestCase):
    """
    ', ' it is important NOT any tag to have it,
    may cause troubles with spliting outline Model 'moje_plemie_skrot', 'przeciwne_plemie_skrot'.
    """
    def setUp(self) -> None:
        self.unallowed_pattern_tag = ', '
        self.tribe = models.Tribe(1, 3109, 'Kaplica', '0, 001', 1, 1, 1, 1, 1,
                                  1)

    def test_All_Tribes_Dont_Have_Unallowed_Pattern_Tag_In_Tag(self):
        try:
            self.tribe.save()
        except ValueError:
            pass
        # Model method save() should not allow to save Tribe with this tag

        self.assertFalse(models.Tribe.objects.all().filter(
            tag__contains=self.unallowed_pattern_tag).exists())
