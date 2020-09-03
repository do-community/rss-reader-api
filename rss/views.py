from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rss.serializers import FeedSerializer, CategorySerializer
from rss.models import RSSFeed, Category
from django.forms.models import model_to_dict
from dateutil import parser

import feedparser

################################################################################
# Feed API Methods                                                             #
################################################################################


class feeds_api(APIView):
    """
    This method returns a list of all the feeds currently subscribed to
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        categories = request.GET.get("category", None)

        rss_feeds = []

        if categories is not None:
            categories = categories.split(",")
            for category in categories:
                try:
                    rss_feed = RSSFeed.objects.get(categories__name=category)
                    rss_feeds.append(rss_feed)
                except RSSFeed.DoesNotExist:
                    pass
        else:
            rss_feeds = RSSFeed.objects.all()

        feeds = []
        for feed in rss_feeds:
            tmp_dict = model_to_dict(feed)
            tmp_dict["categories"] = [x.name for x in feed.categories.all()]
            feeds.append(tmp_dict)

        return Response(feeds, 200)

    def post(self, request):
        params = {}
        status = 200

        feed = FeedSerializer(data=request.data)
        categories = request.data.get("category", None)

        if categories is not None:
            categories = categories.split(",")

        category_objs = []
        for category in categories:
            try:
                cat = Category.objects.get(name=category)
                category_objs.append(cat)
            except Category.DoesNotExist:
                return Response(
                    {
                        "errors": {
                            "category": ["Invalid category {0}.".format(category)]
                        }
                    },
                    400,
                )
        if feed.is_valid() is True:
            feed_obj = feed.save()
            feed_obj.categories.set(category_objs)
            params = model_to_dict(feed_obj)
            params["categories"] = [x.name for x in category_objs]
        else:
            status = 400
            params["errors"] = feed.errors
        return Response(params, status)

    def delete(self, request, feed_id):
        params = {}
        status = 200
        try:
            feed_obj = RSSFeed.objects.get(id=feed_id)
        except RSSFeed.DoesNotExist:
            params["message"] = f"RSS Feed with id {feed_id} does not exist"
            status = 404
            return Response(params, status)

        feed_obj.delete()
        params["message"] = "Feed was successfully deleted"

        return Response(params, status)

    def put(self, request):
        params = {}
        status = 200
        feed_id = request.data.get("id")

        categories = request.data.get("category", None)
        category_objs = []
        if categories is not None:
            categories = categories.split(",")

        if categories is not None:
            category_objs = []
            # If the user is trying to remove all categories and sends empty
            # quotes the splitting code above will make that [""]. So if we
            # see that we know not to look up categories.
            if categories != [""]:
                for category in categories:
                    try:
                        cat = Category.objects.get(name=category)
                        category_objs.append(cat)
                    except Category.DoesNotExist:
                        return Response(
                            {"errors": "Invalid category {0}".format(category)}, 400
                        )
        try:
            feed_obj = RSSFeed.objects.get(id=feed_id)
        except RSSFeed.DoesNotExist:
            params["message"] = f"RSS Feed with id {feed_id} does not exist"
            return Response(params, status)

        feed_dict = model_to_dict(feed_obj)

        feed_dict.update(request.data)
        feed = FeedSerializer(feed_obj, data=feed_dict)
        if feed.is_valid() is True:
            feed_obj_save = feed.save()
            if categories is not None:
                feed_obj_save.categories.set(category_objs)
            params["info"] = model_to_dict(feed_obj_save)
            params["info"]["categories"] = [x.name for x in category_objs]
        else:
            status = 400
            params["errors"] = feed.errors
        return Response(params, status)


class categories_api(APIView):
    """
    This method returns a list of all the feeds currently subscribed to
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        categories = [model_to_dict(x) for x in Category.objects.all()]
        return Response(categories, 200)

    def post(self, request):
        params = {}
        status = 200

        category = CategorySerializer(data=request.data)
        if category.is_valid() is True:
            category_obj = category.save()
            params = model_to_dict(category_obj)
        else:
            status = 400
            params["errors"] = category.errors
        return Response(params, status)

    def delete(self, request, category_id):
        params = {}
        status = 200
        try:
            category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            params["message"] = f"Category with id {category_id} does not exist"
            status = 404
            return Response(params, status)

        category_obj.delete()
        params["message"] = "Category was successfully deleted"

        return Response(params, status)

    def put(self, request):
        params = {}
        status = 200
        category_id = request.data.get("id")

        try:
            category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            params["message"] = f"Category with id {category_id} does not exist"
            return Response(params, status)

        category_dict = model_to_dict(category_obj)

        category_dict.update(request.data)
        category = CategorySerializer(category_obj, data=category_dict)
        if category.is_valid() is True:
            category_obj_save = category.save()
            params = model_to_dict(category_obj_save)
        else:
            status = 400
            params["errors"] = category.errors
        return Response(params, status)


class get_articles(APIView):
    """
    Get latest articles
    """

    def get(self, request):

        count = int(request.GET.get("count", 10))
        categories = request.GET.get("category", None)
        feed_id = categories = request.GET.get("feed", None)

        rss_feeds = []

        if categories is not None:
            categories = categories.split(",")
            for category in categories:
                try:
                    rss_feeds = RSSFeed.objects.filter(categories__name=category)
                except RSSFeed.DoesNotExist:
                    pass
        else:
            rss_feeds = RSSFeed.objects.all()

        articles = []

        if feed_id is not None:
            try:
                rss_feed = RSSFeed.objects.get(id=feed_id)
                rss_feeds = [rss_feed]
            except RSSFeed.DoesNotExist:
                pass

        for feed in rss_feeds:
            if feed.is_visible is False:
                continue
            data = feedparser.parse(feed.url)
            categories = [x.name for x in feed.categories.all()]
            for article in data["entries"][:count]:
                article_data = {}
                article_data["title"] = article["title"]
                article_data["link"] = article["link"]
                # Let's play "What key did they use for date"
                date = article.get("pubDate", None)
                if date is None:
                    date = article.get("published", None)
                    if date is None:
                        date = article.get("updated", None)
                article_data["date"] = parser.parse(date, ignoretz=True)
                article_data["summary"] = article.get("summary", None)
                article_data["feed_name"] = feed.name
                article_data["categories"] = categories
                articles.append(article_data)

        sorted_articles = list(reversed(sorted(articles, key=lambda i: i["date"])))
        return Response(sorted_articles[:count], 200)