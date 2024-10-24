## blog/urls.py
## descruption: URL pattern for the blog app
from django.urls import path
from django.conf import settings
from . import views

urlpatterns =[
  path(r'', views.RandomArticleView.as_view(), name="random" ),
  path(r'show_all', views.ShowAllView.as_view(), name="show_all_blog" ),
  path(r'article/<int:pk>', views.ArticleView.as_view(), name="article" ),
  #path(r'create_comment', views.CreateCommentView.as_view(), name ="create_comment")
  path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name ="create_comment"),
  path(r'create_article', views.CreateArticleView.as_view(), name = 'create_article') #NEW
]