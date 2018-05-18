from django.shortcuts import render,get_object_or_404
from .models import BlogArticles

# Create your views here.
def blog_title(request):
	blogs=BlogArticles.objects.all()
	return render(request,"blog/titles.html",{"blogs":blogs})

def article(request,a_id):
	blog=get_object_or_404(BlogArticles,id=a_id)
	publish_time=blog.publish
	return render(request,"blog/article.html",{'blog':blog,'publish':publish_time})