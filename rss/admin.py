from django.contrib import admin

from rss.models import RSSFeed, Category

admin.site.register(RSSFeed)
admin.site.register(Category)
