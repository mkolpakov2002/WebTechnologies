from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class QuestionManager(models.Manager):
	def new(self):
		return super(QuestionManager, self).get_queryset().order_by("-added_at")

	def popular(self):
		return super(QuestionManager, self).get_queryset().order_by("-rating")

# Create your models here.
class Question(models.Model):
	title = models.CharField(max_length=255, default="")
	text = models.TextField(default="")
	added_at = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)
	author = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.SET_NULL)
	likes = models.ManyToManyField(User, related_name="likes")

	objects = QuestionManager()

	def get_url(self):
		return "/question/" + str(int(self.pk)) + "/"

	class Meta:
		db_table = 'qa_question'

class Answer(models.Model):
	text = models.TextField(default="")
	added_at = models.DateTimeField(auto_now_add=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

	class Meta:
		db_table = 'qa_answer'
