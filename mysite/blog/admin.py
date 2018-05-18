from django.contrib import admin
from .models import BlogArticles

class BlogAdmin(admin.ModelAdmin):
	list_display=['title','author','publish']
	list_filter=['author','publish']
	search_fields=['title','body']
	raw_id_fileds=['author']
	date_hierarchy='publish'
	ordering=['publish','author']
# Register your models here.
admin.site.register(BlogArticles,BlogAdmin)
