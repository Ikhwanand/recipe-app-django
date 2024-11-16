from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class BlogCategories(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title 

    def get_instructions(self):
        # split the instructions by commas and strip whitespace
        if self.instructions:
            steps = [step.strip() for step in self.instructions.split(',')]
            return [step for step in steps]
        return []
    
    def get_ingredients(self):
        # split the instructions by commas and strip whitespace
        if self.ingredients:
            ingredients = [ingredient.strip() for ingredient in self.ingredients.split(',')]
            return [ingredient for ingredient in ingredients]
        return []


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} - {self.rating}"
    

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.recipe.title} - {self.subject}"    
    
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.ForeignKey(BlogCategories, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title 
    

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.subject}"    