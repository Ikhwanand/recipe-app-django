from django import forms
from .models import Recipe, Rating, Comment, BlogPost, Subscription, Contact
from django.contrib.auth.models import User


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title','ingredients', 'instructions', 'image', 'category']
        labels = {
            'title': 'Title',
            'ingredients': 'Ingredients',
            'instructions': 'Instructions',
            'image': 'Image',
            'category': 'Category',
        }
        help_texts = {
            'ingredients': 'Enter the ingredients separated by commas.',
            'instructions': 'Enter the instructions as a comma-separated string. Example: Step 1, Step 2, Step 3',
        }
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 8}),
            'ingredients': forms.Textarea(attrs={'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['category'].widget.attrs.update({'class': 'custom-select my-4'})
    
    def clean_instructions(self):
        instructions = self.cleaned_data.get('instructions')
        if instructions:
            # Split by commas and strip whitespace
            steps = [step.strip() for step in instructions.split(',')]
            # Filter out any empty strings
            steps = [step for step in steps if step]
            # Join the cleaned steps back into a comma-separated string
            cleaned_instructions = ', '.join(steps)
            return cleaned_instructions
        return instructions
    
    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients')
        if ingredients:
            # Split by commas and strip whitecase
            steps = [step.strip() for step in ingredients.split(',')]
            # Filter out any empty strings
            steps = [step.strip() for step in steps if step]
            # Join the cleaned steps back into a comma-separated string
            cleaned_ingredients = ', '.join(steps)
            return cleaned_ingredients
        return ingredients
        
   
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating 
        fields = ['rating']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['name', 'email', 'subject', 'message']
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'category']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter title'})
        self.fields['content'].widget.attrs.update({'placeholder': 'Enter content'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['category'].widget.attrs.update({'class': 'custom-select my-4'})
        
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
        
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    