from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import register_view, login_view, logout_view, Home , read_all_blogs_view, edit_blog_view, create_blog, read_detailed_blog_view, profile_view, search_view

urlpatterns = [
    path('home/', Home, name="home"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>',profile_view,name="profile"),
    path('read_blogs',read_all_blogs_view, name="read_all_blogs"),
    path('create/',create_blog,name="create_blog"),
    path('blogs/<str:title>/', read_detailed_blog_view, name="detailed_blog"),
    path('<int:pk>/edit', edit_blog_view, name="edit_blog"),
    path('search/',search_view,name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)