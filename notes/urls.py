from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
       path('', views.post_list, name='post_list_url'),
       path('post/create/', views.PostCreate.as_view(), name='post_create_url'),
       path('post/<str:slug>/', views.PostDetail.as_view(), name='post_detail_url'),
       path('post/<str:slug>/update/', views.PostUpdate.as_view(), name='post_update_url'),
       path('favorites/', views.favorites, name='favorites'),
       path('unfavorites/', views.unfavorites, name='unfavorites'),
       path('deleting_post/', views.deleting_post, name='deleting_post'),
       url(r'^sorting_notes/$', views.sorting_notes, name='sorting_notes'),
       path('filter_by_favorites/', views.filter_by_favorites, name='filter_by_favorites'),
       path('filter_by_date/', views.filter_by_date, name='filter_by_date'),
       path('filter_by_category/', views.filter_by_category, name='filter_by_category'),
       path('search_by_title/', views.search_by_title, name='search_by_title'),
]