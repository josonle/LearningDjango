## LearningDjango

### Why should i decide to learn the Django?
想学习python的web框架有一段时间了，自上次寒假开始就有这样的计划，也为此付之行动了一段时间，但倒是还是贪玩，慢慢就荒废了。而选择django也是综合考虑了一番，那就启程吧！！！

参考资料：
> 《跟老齐学Python Django实战》
> 
> 《Django实践18课》
> 
> 参照追梦和刘江的blog
> 
> 官方文档

环境配置：
> Python3.6
> django1.10

### 第一天
#### Let's go！！！
- 创建项目Project
命令行下使用 `django-admin startproject Project_name` ，这里我的项目是mysite
- 创建应用APP
命令行下使用 `django-admin startapp app_name` ，这里我的 app_name 是 blog
> 或者使用 `python manage.py startapp app_name`
> django-admin.py是安装django后有的，bin目录下，而项目目录下的manage.py封装了django-admin的操作
> 

  OK,查看刚刚创建的项目结构：
  ![](D:\火狐软件下载目录\Markdown汇总\MD图片\django001.png)
从图片可看出，生成了 `mysite`,`blog`文件夹和`manage.py`。
再分别查看 `mysite`,`blog` 结构，如下图：
  ![](D:\火狐软件下载目录\Markdown汇总\MD图片\django002.png)
  ![](D:\火狐软件下载目录\Markdown汇总\MD图片\django003.png)
结构解释：

- manage.py
就是封装了一些命令的工具，如上面所述的django-admin。
- mysite 具有管理项目的功能
    + settings.py：项目初始化、参数配置等文件
    + urls.py：路由配置文件，使得 url 能指向某个函数或视图（template）
    + wsgi.py：提供底层的网络通信功能，可百度一下WSGI
    + __init__.py:使得mysite变成可以import的库
- blog 创建的应用
    + _init.py_:类似上面的
    + admin.py:管理工具，如可以向管理增加新应用
    + apps.py:没啥用
    + models.py:定义应用的数据模型
    + tests.py:测试用的
    + views.py:定义视图函数、视图类
    + migrations:存储数据库表结构的指令
这里我们要明确，不止创建一个APP
#### 基本配置
```py
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 开发模式DEBUG设置为True，运行时可以显示错误信息
# 但生产环境必须修改为False
ALLOWED_HOSTS = []
#填写主域名，使网站可被访问。开发模式下可为空

# Application definition
# 这里填入你创建的应用名，如blog，才能告诉django这是我们一伙的
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]

```
数据库配置,这里使用默认的SQLite。你可能还没看到SQLite的影子，稍等一会儿。
```py
# Database
# 可参考官方文档其余数据库配置
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
时区语言等
```py
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```
#### 运行项目
命令行下 `python manage.py runserver`
![](D:\火狐软件下载目录\Markdown汇总\MD图片\004.png)
打开http://127.0.0.1:8000/。
![](D:\火狐软件下载目录\Markdown汇总\MD图片\005.png)
如图所示，成功踏出第一小步了！！！
这时你会发现 mysite 根目录下生成了 db.sqlite3 文件，这就是我们的数据库了。

#### 数据模型的确定及编写
我们搭建一个web项目前，要明确需要实现那些功能，对吧。而model也就对应这些功能。
我们这里只是简单编写博客，只需要管理博客的类就好了。

##### 切换到 blog 目录下，编写 models.py
```py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class BlogArticles(models.Model):#继承自models.Model
    #字段和其属性
    title=models.CharField(max_length=30)
    author=models.ForeignKey(User,related_name="blog_posts")
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)

    class Meta:
        #按照publish逆顺序显示
        ordering=("-publish")

    def __str__(self):
        #为了在页面中不单调显示，而显示文章标题
        return self.title
```
首先要明确，在Django中不需直接编写SQL语句，django能完成相应的数据库操作。

你能从代码中看到我们定义了 title、author等属性，在数据库表中把它们称作**字段**。而字段又有属性，形如 CharField() 。

注意，ordering 必须是列表或元组，要有逗号。

- 建立数据库表
命令行下`python manage.py makemigrations`
> PS D:\PyCharm 2017.3\PyProjects\LearningDjango\mysite> python3 manage.py makemigrations
Migrations for 'blog':
  blog\migrations\0001_initial.py
    -Create model BlogArticles

查看一下00001_initial.py，可发现,就是定义了一般的数据库表和操作方式。

```py
        migrations.CreateModel(
            name='BlogArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('body', models.TextField()),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            options={
                'ordering': ('-publish',),
            },
    ]
```

- 创建数据库
命令行下 `python manage.py migrate`， OK，模型对应的数据库就创建好了。

- 在 admin.py 中注册该数据模型
```py
from django.contrib import admin
# 引入blog模型
from .models import BlogArticles
# Register your models here.
admin.site.register(BlogArticles)#注册
```

你也能在admin.py增加一些内容
```py
from django.contrib import admin
from .models import BlogArticles
class BlogAdmin(admin.ModelAdmin):
    list_display=['title','author','publish']
    list_filter=['author','publish']
    #search_fields=['title','body']#搜索框
    raw_id_fileds=['author']
    date_hierarchy='publish'
    ordering=['publish','author']
# Register your models here.
admin.site.register(BlogArticles,BlogAdmin)
```
##### 创建超级管理员以便登录并发表网站
命令行下 `python manage.py createsuperuser` ，并相应创建密码等。
创建好后，浏览器打开 http://127.0.0.1:8000/admin/ ，用刚创建的用户名密码登录即可。

你能看到有个 BLOGARTICLES 选项，可以增加文章。
![](D:\火狐软件下载目录\Markdown汇总\MD图片\006.png)

***
### 第二天
#### 视图的编写,模板的应用及URL的匹配
类似scrapy的交互式环境，也可以在django交互环境中测试。
`python manage.py shell`
如下是一些示列，对数据库中模型的操作
```py
from blog.models import BlogArticle#从app的models中导入模型类
blogs=BlogArticle.objects.all()#通过这个获取所有数据
#len(blogs)文章数量
#blogs[0].title,body,author获取第一篇文章标题等

```
所以我们可以在代码中类似使用这些，对数据库的数据操作

先在views.py中编写一个视图函数，把文章能显示在网页上
```py
from django.shortcuts import render
from .models import BlogArticles

# Create your views here.
def blog_title(request):
    blogs=BlogArticles.objects.all()
    return render(request,"blog/titles.html",{"blogs":blogs})
    
```

- **render(request,templates,参数)**
    + request必须的，且在第一位
    + template指的是模板文件位置
    + 参数是要向模板中传递的参数，只能通过字典形式

- 模板：数据信息为了美观地展示在网页上，就得通过前端模板才行
    + 模板文件语法
        * {{变量}}
        * {%block name%}{%endblock%},块标签，name是名称
        * {%extends  模板name%}，继承自某个模板就对应那个模板的name
        * {%for one in series%}{%endfor%}

OK，现在我们可以编写模板文件了。

***
此处省略
***
URL配置<urls.py>
个人感觉并不难，就是一个url正则匹配的过程。它分为两种，其一是在 `mysite` 项目的总的 `urls.py` 中进行管理；其二是在不同应用中创建新的`urls.py`，通过引入 `include` 把匹配任务分散，便于管理url。

```py
#mysite/urls.py中
from django.conf.urls import url,include#引入include
from django.contrib import admin
#除去include，其他都是通用的
urlpatterns=[
    url(r'^admin/',admin.site.urls),#默认
    url(r'^blog/',include('blog.urls',namespce='blog',app_name='blog')),
]
#这就是url匹配列表，就这样写的。
#正则匹配这块如r'^blog/'，代表以/blog/开始匹配。还有就是$代表以什么结尾
#include(app.urls)表示除去blog/，之后的匹配任务分给app中的urls.py，而namespace、app_name貌似就是个标识

```
而关键是url(匹配项，对应视图对象)，比如
```py
from django.conf.urls import url
from . import views#引入视图函数
urlpatterns=[
    url(r'^$',views.blog_title,name='blog_title'),
]
```
对应上面include的应用，如果url匹配到了，就只想views.py中的视图函数（类），name就是个区分标识。

#### 总结views、urls、templates
一旦生成一个 request ，就会有一个 url 匹配过程。
匹配成功，就通过 urls.py 对应不同的 views，views 一旦接收到了 request 就转向去加载一个模板文件，并传入需要的参数，接着便是 response ，网页就显示出来了。
匹配不成功，有函数 get_object_or_404(),同样是对应的 response 。

自我感觉现在就是不会编写模板，o(╥﹏╥)o

![这张图更清晰体现](https://user-gold-cdn.xitu.io/2018/1/30/16145fbf830a5eac?w=575&h=751&f=png&s=113539 "Optional title")

[django从请求到响应](https://blog.csdn.net/l_vip/article/details/79182063)，他的其他几篇博客也可学习。

### 5.13sublime记录
今天为了可以交互环境运行py3，对sublimePERL的config进行了修改。
> 进入方式：首选项->浏览插件目录->选择sublimePERL下的config->创建文件夹Python3，并将原有Python下文件复制到了Python3下->修改Main.sublime-menu下其中所有"cmd":所在的那一行的"python"改为"py","-3",->其次，Default.sublime-commands下所有"file"，"caption"路径的Python改为"Python3"。
>  

但"工具->subimePERL"下没有Python3选项。
等待明天看看是否有。。。

其次"首选项->快捷键设置"
```py
[
    {"keys":["f5"],
"caption": "SublimeREPL: Python - RUN current file",
"command": "run_existing_window_command", "args":
{
"id": "repl_python_run",
"file": "config/Python/Main.sublime-menu"
}}
]
#"caption": "SublimeREPL: Python - RUN current file",
#这一步关键，工具->sublimePERL->Python->RUN current file
```
https://www.zhihu.com/question/42102873

### 第三天
#### 内容补充
前面讲到了如何直接对数据库的操作
```py
# 命令行 python manage.py shell
from blog.models import BlogArtiles
blogs=BlogArticles.objects.all() #获取数据库中所有数据项

```
它的类型 `django.db.models.query.QuerySet`，你可以通过for 循环，对其每一项数据进行操作，如：
```py
for blog in blogs:
    print(blog.title)
    print(blog.body)
    print(blog.author.username)
    print(blog.publish)
```
没错，打印的都是 BlogArticles 中定义的字段。

然后我又看到了一种写法
```py
blog=BlogArticles.objects.get(id=1)
#这个id就是文章编号，就好比上面的 for 循环，第一遍对应 id=1
#同理对应字段对应格式
blog.title
blog.body
。。。

```
然后在上面我们定义的 titles.html 中，就能通过这样实现点击相应的标题跳转到对应的文章了。
你应该会想到万一 id 超过文章数量怎么办吧？加一个404页面就好了。而 django 中正好有`get_object_or_404()`方法。用法如下：

```py
from django.shortcuts import get_object_or_404,render#没错，这家伙和render是一伙的
blog=get_object_or_404(BlogArticles,id)
```

OK，再次编写一个视图函数对应blog的跳转。
```py
def article(request,a_id):#多一个参数，url该如何配置？
    blog=get_object_or_404(BlogArticles,id=a_id)
    publish_time=blog.publish_time#嗯，作者就是这样写的，虽然可以直接传一个参数过去.
    return render(request,"blog/article.html",{'blog':blog,'publis':publish_time})
```

按上次的思路，接下来便是 url 匹配，template 编写。我前端不行，这块代码直接在文末贴出来吧，以后都如此。

像我上面代码中注释的，该如何匹配？首先明确，希望 url 类似 `./blog/1/`。
直接说吧，(?P<name>匹配形式)这里的 name 对应着视图函数中参数名，如(?P<a_id>\d>) 用来匹配参数 id， a_id 在 `def article(request,a_id)` 这。
所以如下添加 url 路径
```py
urlpatterns=[
    url(r'^$',views.blog_title,name='blog_title'),
    url(r'(?P<a_id>\d+)/$',views.article,name='blog_detail')
]
```

> 注意，传进的参数都是字符串，都是字符串。
> （？P<name>regx）:正则会匹配到括号括起的内容（regx要匹配的）作为参数传给视图函数，而 name 则指明是哪个参数。
> 
#### 返回 Response 写法
- 最原始的导入 `HttpResponse` 和 `Http404`，类似：

```py
from django.http import HttpResponse,Http404
from django.template import loder#用于数据项加载 template
from .models import BlogArticles
def Func(request,id):
    try:
        blog=BlogArticles.objects.get(id=id)
    except BlogArticles.DoesNotExist:
        raise Http404("文章不存在。。。")
    template=loder.get_template(模板文件)
    data={'blog':blog,'publish':blog.publish_time}
    return HttpResponse(template.render(data,request))
```
- 整个一个加载模板并传递参数的流程，挺繁琐的。那就用简单点的吧，像前几次文章中的，引入`render` 和 `get_object_or_404` ，我就不写了，你往前翻翻吧。

### 总结
#### 对于 URL 设计思考
- 建议分多级路由进行 url 匹配，也便于管理
    + include()的使用
> 明确URLConf机制先从项目根 urls 即 mysite.urls 开始匹配urlpatterns
> url(regx,include('app.urls',namespace,app_name))
> include还有一种用法，比如 /blog/python/,/blog/c++/,/blog/java/等类似前缀相同的情况下，可以定义一个 mypatterns，如下。
> 
```py
mypatterns=[
    url(r'^python/',视图),
    url(r'^python/',视图),
    ...
]
urlpatterns=[
    url(r'^blog/',include(mypatterns))
]
```
- url 中含有需要传入参数的情况
    + `（？P<name> regxpattern）` 的使用（可以有多个）。
    + 从上一级 URLconf 匹配到的参数依旧会传到下一级（就是最终函数都能收到）。
- 视图中需要的参数不在url中时
    + 通过`url(regx,view,data)`，额外的参数data允许以字典形式传入
    + 如上形式也能传递给 `include()`，但会传给include包含的每一个 urlconf的视图函数。**如果某个视图不需要改参数，反而会报错**。
    + 避免data中参数名与url中匹配的参数名重名冲突。
#### URL反解
> 为了解决这个问题，Django提供了一种解决方案，只需在URL中提供一个name参数，并赋值一个你自定义的、好记的、直观的字符串。
通过这个name参数，可以反向解析URL、反向URL匹配、反向URL查询或者简单的URL反查。
在需要解析URL的地方，对于不同层级，Django提供了不同的工具用于URL反查：

> 在模板语言中：使用 url 模板标签。(也就是写前端网页时）

> 在Python代码中：使用 reverse() 函数。（也就是写视图函数等情况时）

> 在更高层的与处理Django模型实例相关的代码中：使用 get_absolute_url() 方法。(也就是在模型model中)
> 
> 出自 http://www.liujiangblog.com/course/django/136
> 

先说模板标签的吧，按我的理解分两种：

- 定义了别名 name，如{%url '别名' 参数%}
`<a href="{% url 'blog_detail' 2%}">  ` 对应 `url(r'(?P<a_id>\d+)/$',views.article,name='blog_detail')`

- 定义了命名空间 namespace 和别名 name，{%url 'namespace:name' 参数%}。为了区别同 name 而不同 namespace的匹配，namespace 可换成 app_name。
```py
#可以在urls.py中定义
app_name=blog
#模板中
<a href="{% url 'blog:blog_detail' 2%}">
#仍旧对应 url(r'(?P<a_id>\d+)/$',views.article,name='blog_detail')
```

而 reverse()用法如下
```py
####urls
from django.conf.urls import url,include
from app1 import views
urlpatterns = [
    url(r'^art/', views.art3, name='blog'),
]
####views
def art3(request):
    print(reverse('blog'))    #在视图函数中对url进行反向解析
    return HttpResponse("OK")
```

### 第四天