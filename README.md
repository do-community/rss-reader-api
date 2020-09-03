# rss-reader-api
RSS Reader API written in Django Rest. This app provides a REST API using the 
Django Rest Framework that aggregates articles from RSS feeds. This will allow 
you to create a system of news delivery that is appropriate for you.

## How To Use It
As a user you will be able to save RSS feeds from your favorite sites and have
all of the data aggregated into a single news feed. You can take it one step 
further and set categories for each feed and filter the articles based on 
category. Categories are not required, but add the ability to customize your
feed even more.

## API Spec
All examples are using [`httpie`](https://httpie.org/). If you haven't checked 
it out you should.

Below are all of the public endpoints currently available.

**Note:** - All API methods end with a `/`. If you attempt to call an API method
without this you will receive a 404.


### POST `/login/`
Retrieve a users API token

*Parameters*

* `username` - Your username
* `password` - Your Password

*Example*

`http POST https://example.api/obtain-auth-token/ username=user password=pass`

*Returns*

```
{
    "token": "YOUR_API_TOKEN"
}
```

### GET `/articles/`
Fetch articles from your news sources.

*Query Parameters*

* `category` (optional) - filter the results based on your categories. This
can be a single value or a comma separated list. Note that categories are case
sensitive.
* `count` (optional) - The total number of articles to fetch.

*Example*

`http https://example.api/articles/?category=Tech&count=10`

*Returns 200*
```json
[
    {
        "categories": [
            "Tech"
        ],
        "date": "DATE",
        "feed_name": "FEED_AS_SPECIFIED_BY_YOU",
        "link": "LINK",
        "summary": "SUMMARY TEXT",
        "title": "TITLE"
    }
    ...
]
```

### GET `/feeds/`
Returns a list of all of the feeds currently being aggregated.

*Query Parameters*

* `category` (optional) - filter the results based on your categories. This
can be a single value or a comma separated list. Note that categories are case
sensitive.

*Example*

`http https://example.api/feeds?category=Tech`

*Returns 200*
```json
[
    {
        "categories": [],
        "id": 1,
        "is_visible": true,
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage"
    },
    ...
]
```

### POST `/feeds/` - **Auth Required**
Add an RSS feed. Articles from this feed will be aggregated into the others

*Parameters*

* `name` - The name you wish to give this source
* `url` - The URL of the RSS feed
* `categories` - The category(ies) to associate the feed with. This can be a
single category or a list of categories spearated by a `,`
* `is_visible` - Whether or not you want news from this source to be visible (optional)

*Example*

`http POST https://example.api/feeds/ 'Authorization: Token '$TOKEN name="Mason Egger's Website" url="https://mason.dev/index.html" category="Tech,Python"`

*Returns 200*
```json
{
    "categories": [
        "Tech",
        "Python"
    ],
    "id": 5,
    "is_visible": true,
    "name": "My Feed",
    "url": "https://demo.shark.codes"
}
```

*Returns 400*
```
{
    "errors": {
        "name": [
            "This field is required."
        ],
        "url": [
            "This field is required."
        ]
        "category": [
            "Invalid catogory CATEGORY."
        ]
    }
}
```

### PUT `/feeds/` - **Auth Required**
Update an RSS feed.

*Parameters*

* `id` - The ID of the category
* `name` (optional) - The name you wish to give this source
* `url` (optional) - The URL of the RSS feed
* `is_visible` (optional) - Whether or not you want news from this source to be 
visible
* `category` (optional) - The category you want to associate with this feed.
This can be a single category or a list of categories spearated by a `,` 

*Example*

`http PUT https://example.api/feeds/ 'Authorization: Token '$TOKEN id=16 name="Awesome Blog" category="Tech"`

*Returns*
```json
{
    "info": {
        "categories": [
            "Tech"
        ],
        "id": 16,
        "is_visible": true,
        "name": "dog",
        "url": "https://mason.dev/"
    },
}
```

### DELETE `/feeds/<int:feed_id>` - **Auth Required**
Delete an RSS feed. Articles from this feed will no longer appear.

*URI Parameters*

* `feed_id` - The ID of the feed to delete

*Example*

`http DELETE http://localhost:8000/feeds/<FEED_ID>/ 'Authorization: Token '$TOKEN`

*Returns 200*
```json
{
    "message": "Feed was successfully deleted",
}
```

*Returns 404*
```json
{
    "message": "Class with id 5 does not exist",
}
```

### GET `/categories/`
Returns a list of all of the categories currently available

*Parameters*

None

*Example*

`http https://example.api/categories`

*Returns 200*
```json
[
    {
        "id": 1,
        "name": "Tech"
    },
    ...
]
```

### POST `/categories/` - **Auth Required**
Add a a category. RSS Feeds can be tagged with categories to aide with filtering.

*Parameters*

* `name` - The name you wish to give this category


*Example*

`http POST https://example.api/categories/ 'Authorization: Token '$TOKEN name="Sports"`

*Returns 200*
```json
{
    "id": 3,
    "name": "Sports"
}
```

*Returns 400*
```
{
    "errors": {
        "name": [
            "This field is required."
        ],
    }
}
```

### PUT `/category/` - **Auth Required**
Update a category.

*Parameters*

* `id` - The ID of the category
* `name` - The name you wish to give this category


*Example*

`http PUT https://example.api/category/ 'Authorization: Token '$TOKEN id=3 name="Sportz"`

*Returns 200*
```json
{
    "id": 3,
    "name": "Sportz"
}
```

### DELETE `/category/<int:category_id>` - **Auth Required**
Delete a category. RSS Feeds will no longer be associated with this category

*URI Parameters*

* `feed_id` - The ID of the category to delete

*Example*

`http DELETE http://localhost:8000/category/<CATEGORY_ID>/ 'Authorization: Token '$TOKEN`

*Returns 200*
```json
{
    "message": "Category was successfully deleted",
}
```

*Returns 404*
```json
{
    "message": "Category with id 3 does not exist"
}
```
--- 

## Create a Secret key
```python
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```