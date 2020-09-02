from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class RSSFeed(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField(max_length=512)
    is_visible = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        verbose_name = "RSS Feed"
        verbose_name_plural = "RSS Feeds"

    def __str__(self):
        return self.name
