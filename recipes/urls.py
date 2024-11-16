from django.urls import path 
from . import views

app_name = 'recipes'
urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path('about/', views.to_about, name='about'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('recipes/', views.recipes_list, name='recipes_list'),
    path('create/', views.recipe_create, name='recipe_create'),
    path('update/<int:pk>/', views.recipe_update, name='recipe_update'),
    path('delete/<int:pk>/', views.recipe_delete, name='recipe_delete'),
    path('detail/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blogs/update/<int:pk>/', views.blog_update, name='blog_update'),
    path('blogs/delete/<int:pk>/', views.blog_delete, name='blog_delete'),
    path('blogs/detail/<int:pk>/', views.blog_detail, name='blog_detail'),
]

