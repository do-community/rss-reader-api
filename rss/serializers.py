from rest_framework import serializers
from rss.models import RSSFeed, Category


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSSFeed
        fields = [
            "name",
            "url",
            "is_visible",
        ]
        extra_kwargs = {
            "is_visible": {"required": False},
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
