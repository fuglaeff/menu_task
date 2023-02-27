from django.core.exceptions import ValidationError
from django.db import models


class Menu(models.Model):
    slug = models.SlugField(max_length=255, primary_key=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('slug',)


class Folder(models.Model):
    slug = models.SlugField(max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='folders'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['menu', 'slug'], name='unique_folder_slug_in_menu'),
        ]

        ordering = ('slug', )

    def clean(self):
        if self.parent and self.parent.menu != self.menu:
            raise ValidationError('Parent menu must eq menu')

    def __str__(self):
        return self.slug
