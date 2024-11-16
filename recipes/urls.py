from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Recipe URLs
    path('', views.recipe_list, name='recipe_list'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<slug:slug>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<slug:slug>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('favorite-recipes/', views.favorite_recipes, name='favorite_recipes'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Profile URLs
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    
    # Other URLs
    path('about/', views.to_about, name='about'),
]
