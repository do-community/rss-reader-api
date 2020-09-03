from django.urls import path
from . import views

app_name = "rss"

urlpatterns = [
    path("categories/", views.categories_api.as_view(), name="categories"),
    path(
        "categories/<int:category_id>/",
        views.categories_api.as_view(),
        name="delete_categories",
    ),
    path("feeds/", views.feeds_api.as_view(), name="feeds"),
    path("feeds/<int:feed_id>/", views.feeds_api.as_view(), name="delete_feeds"),
    path("articles/", views.get_articles.as_view(), name="articles"),
]