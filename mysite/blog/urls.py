from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.blog_title,name='blog_title'),
	url(r'(?P<a_id>\d+)/$',views.article,name='blog_detail')
]