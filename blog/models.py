from django.db import models
from datetime import datetime
from django.utils import timezone
from .slugify_to_russian import slugify_rus
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404


class Post(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	text = models.CharField(max_length=30000, unique=False)
	slug = models.SlugField(max_length=100, blank=True, unique=True)
	non_unique_slug = models.SlugField(max_length=100, blank=True, unique=False)
	likes = models.BigIntegerField(default=0)
	for_view = models.CharField(default="false", max_length=10)
	pub_date = models.DateTimeField(default=timezone.now)
	who_liked = models.ManyToManyField(User, blank=True, related_name='who_likid')
	def save(self):
		if not self.slug:
			self.slug = slugify_rus(self.name)
		self.non_unique_slug = self.slug
		try:
			super().save()
		except IntegrityError:
			posts_with_the_same_slug = list(Post.objects.all().filter(non_unique_slug=self.non_unique_slug))
			self.slug += "_" + str(len(posts_with_the_same_slug) + 1)
			super().save()
	def __str__(self):
		return self.name