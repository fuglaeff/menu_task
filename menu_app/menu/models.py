from django.db import models
from django.core.exceptions import ValidationError


class Menu(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Folder(models.Model):
    name = models.CharField(max_length=50)
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
            models.UniqueConstraint(
                fields=['name', 'parent'], name='unique_folder_name_in_parents_folder'),
        ]

        ordering = ('name', )

    def clean(self):
        if self.parent and self.parent.menu != self.menu:
            raise ValidationError('Parent menu must eq menu')

    def __str__(self):
        return self.name
