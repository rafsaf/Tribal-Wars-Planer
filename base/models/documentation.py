from django.db import models
from markdownx.models import MarkdownxField


class Documentation(models.Model):
    """Docs page"""

    title = models.CharField(max_length=30)
    main_page = MarkdownxField()
    language = models.CharField(max_length=2, default="pl")

    def __str__(self):
        return f"{self.title}_{self.language}"

    class Meta:
        ordering = (
            "-language",
            "title",
        )
