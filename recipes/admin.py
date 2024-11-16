from django.contrib import admin
from .models import Recipe, Categories, Rating, Comment, BlogPost, Subscription, Contact, BlogCategories

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Categories)
admin.site.register(BlogCategories)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(BlogPost)
admin.site.register(Subscription)
admin.site.register(Contact)
