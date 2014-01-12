# -*- coding: utf-8 -*-
from mock import patch

from django.contrib.sites.models import Site
from django.test import TestCase

from planet.models import Post
from planet.tests.factories import (
    BlogFactory, FeedFactory, PostFactory, AuthorFactory
)


class BlogViewsTest(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()
        self.blog = BlogFactory.create(title="Blog-1")
        self.feed = FeedFactory.create(title="Feed-1", site=self.site, blog=self.blog)

    def test_list(self):
        response = self.client.get("/blogs/")
        self.assertEquals(response.status_code, 200)

    def test_detail(self):
        response = self.client.get("/blogs/1/")
        self.assertEquals(response.status_code, 301)

        response = self.client.get("/blogs/1/blog-1/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/blogs/2/other-blog/")
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        self.blog.delete()
        self.feed.delete()


class FeedViewsTest(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()
        self.feed = FeedFactory.create(title="Feed-1", site=self.site)

        self.post = PostFactory.create(feed=self.feed)
        self.post.tags = "tag1, tag2"

    def test_list(self):
        response = self.client.get("/feeds/")
        self.assertEquals(response.status_code, 200)

    def test_detail(self):
        response = self.client.get("/feeds/1/")
        self.assertEquals(response.status_code, 301)

        response = self.client.get("/feeds/1/feed-1/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/feeds/2/other-feed/")
        self.assertEquals(response.status_code, 404)

    def test_feed_tags(self):
        response = self.client.get("/feeds/1/feed-1/tags/tag1/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/feeds/1/feed-1/tags/tag2/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/feeds/1/feed-1/tags/tag3/")
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        self.feed.delete()
        self.post.delete()


class PostViewsTest(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()
        self.feed = FeedFactory.create(title="Feed-1", site=self.site)
        self.post = PostFactory.create(feed=self.feed)

    def test_list(self):
        response = self.client.get("/posts/")
        self.assertEquals(response.status_code, 200)

    def test_detail(self):
        response = self.client.get("/posts/1/")
        self.assertEquals(response.status_code, 301)

        response = self.client.get("/posts/1/post-1/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/posts/2/other-post/")
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        self.post.delete()
        self.feed.delete()


class AuthorViewsTest(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()
        self.feed = FeedFactory.create(title="Feed-1", site=self.site)
        self.author = AuthorFactory.create(name="Author-1")
        self.post_list = PostFactory.create_batch(size=3, feed=self.feed, authors=[self.author])

    def test_list(self):
        response = self.client.get("/authors/")
        self.assertEquals(response.status_code, 200)

    def test_detail(self):
        response = self.client.get("/authors/1/")
        self.assertEquals(response.status_code, 301)

        response = self.client.get("/authors/1/author-1/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/authors/2/other-author/")
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        self.author.delete()
        self.feed.delete()


class TagViewsTest(TestCase):

    def setUp(self):
        self.site = Site.objects.get_current()
        self.feed = FeedFactory.create(title="Feed-1", site=self.site)
        self.post = PostFactory.create(feed=self.feed)
        self.post.tags = "tag1, tag2"

    def test_list(self):
        response = self.client.get("/tags/")
        self.assertEquals(response.status_code, 200)

    def test_feed_list(self):
        response = self.client.get("/tags/tag1/feeds/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/tags/tag3/feeds/")
        self.assertEquals(response.status_code, 404)

    def test_author_list(self):
        response = self.client.get("/tags/tag1/authors/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/tags/tag3/authors/")
        self.assertEquals(response.status_code, 404)

    def test_detail(self):
        response = self.client.get("/tags/tag1/")
        self.assertEquals(response.status_code, 200)

        response = self.client.get("/tags/other-tag/")
        self.assertEquals(response.status_code, 404)

    def tearDown(self):
        self.post.delete()
        self.feed.delete()