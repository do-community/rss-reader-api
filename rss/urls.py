from django.urls import path
from . import views

app_name = "rss"

urlpatterns = [
    path("category/", views.get_category.as_view(), name="get_category"),
    path("category/add/", views.create_category.as_view(), name="create_category"),
    path("category/update/", views.update_category.as_view(), name="update_category"),
    path(
        "category/delete/<int:category_id>/",
        views.delete_category.as_view(),
        name="delete_category",
    ),
    path("feeds/", views.get_feeds.as_view(), name="get_feeds"),
    path("feeds/add/", views.create_feed.as_view(), name="create_feeds"),
    path(
        "feeds/delete/<int:feed_id>/", views.delete_feed.as_view(), name="delete_feeds"
    ),
    path("feeds/update/", views.update_feed.as_view(), name="update_feeds"),
    path("articles/", views.get_articles.as_view(), name="get_articles"),
]