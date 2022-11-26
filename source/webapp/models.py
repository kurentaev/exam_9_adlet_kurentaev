from django.contrib.auth import get_user_model
from django.db import models


class Photo(models.Model):
    photo = models.ImageField(
        upload_to='photos',
        verbose_name='Photo',
        null=False,
        blank=False
    )
    description = models.CharField(
        max_length=100,
        verbose_name='Description',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )
    author = models.ForeignKey(
        to=get_user_model(),
        verbose_name='Author',
        related_name='avatars',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author}"

    class Meta:
        db_table = "photo"
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        ordering = ['-created_at', ]
