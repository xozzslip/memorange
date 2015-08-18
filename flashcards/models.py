from django.db import models
from datetime import datetime
from django.utils import timezone
from .slugify_to_russian import slugify_rus
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	def __str__(self):
		return "%s's profile" % self.user

class RepeatTime(models.Model):
	time = models.DurationField()
	def __str__(self):
		return str(self.time)

class Deck(models.Model):
	deck_name = models.CharField(max_length=30) 
	slug = models.SlugField(max_length=30, blank=True, unique=False)
	repeat = models.ManyToManyField(RepeatTime)
	owner = models.ForeignKey(User)
	class Meta:
		unique_together = (("owner", "slug"),)
	def save(self):
		self.slug = slugify_rus(self.deck_name)
		super().save()
	def __str__(self):
		return self.deck_name

class Question(models.Model):
	question_text = models.CharField(max_length=200, unique=False)
	answer_text = models.CharField(max_length=500, blank=True)
	deck = models.ForeignKey(Deck)
	pub_date = models.DateTimeField(default=timezone.now)
	repition_number = models.IntegerField(default=0)
	last_repeat = models.DateTimeField(default=timezone.now)
	next_repeat = models.DateTimeField(blank=True, null=True)
	class Meta:
		unique_together = (("question_text", "deck"),)
	def save(self):
		if self.repition_number < len(self.deck.repeat.all()):
			self.next_repeat = self.last_repeat + self.deck.repeat.all().order_by('time')[self.repition_number].time
			super().save()
		else:
			self.next_repeat = self.last_repeat + self.deck.repeat.all().order_by('time')[-1].time
			super().save()
	def __str__(self):
		return self.question_text

