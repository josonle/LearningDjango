from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User#User是django默认的，指的是创建的用户

# Create your models here.

class BlogArticles(models.Model):
	#字段和其属性
	title=models.CharField(max_length=30)
	author=models.ForeignKey(User,related_name="blog_posts")
	body=models.TextField()
	publish=models.DateTimeField(default=timezone.now)

	class Meta:
		#按照publish逆顺序显示
		ordering=('-publish',)

	def __str__(self):
		#为了在页面中不单调显示，而显示文章标题
		return self.title
