from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Q
from django.contrib.auth.models import User
from .models import (
    Recipe, Rating, Comment, BlogPost, Categories, FavoriteRecipe,
    UserProfile, BlogCategories
)
from .forms import (
    RecipeForm, RatingForm, CommentForm, BlogPostForm,
    SubscriptionForm, ContactForm, CategoryForm, UserProfileForm
)

def recipe_list(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-created_at')
    categories = Categories.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        recipes = recipes.filter(category=category)
    
    paginator = Paginator(recipes, 9)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'selected_category': category_slug
    }
    return render(request, 'recipes/recipe_list.html', context)

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipes:recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Create Recipe'
    })

def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ratings = recipe.ratings.all()
    comments = recipe.comments.all().order_by('-created_at')
    user_rating = None
    is_favorite = False
    
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()
        is_favorite = FavoriteRecipe.objects.filter(recipe=recipe, user=request.user).exists()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to interact with recipes.')
            return redirect('account_login')
        
        if 'rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.recipe = recipe
                rating.user = request.user
                rating.save()
                messages.success(request, 'Rating added successfully!')
                return redirect('recipes:recipe_detail', slug=slug)
        
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added successfully!')
                return redirect('recipes:recipe_detail', slug=slug)
    
    rating_form = RatingForm(instance=user_rating)
    comment_form = CommentForm()
    
    context = {
        'recipe': recipe,
        'ratings': ratings,
        'comments': comments,
        'rating_form': rating_form,
        'comment_form': comment_form,
        'user_rating': user_rating,
        'is_favorite': is_favorite,
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        messages.error(request, 'You can only edit your own recipes.')
        return redirect('recipes:recipe_detail', slug=slug)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipes:recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Edit Recipe',
        'recipe': recipe
    })

@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        messages.error(request, 'You can only delete your own recipes.')
        return redirect('recipes:recipe_detail', slug=slug)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipes:recipe_list')
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

@login_required
def toggle_favorite(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    favorite, created = FavoriteRecipe.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )
    
    if not created:
        favorite.delete()
        messages.success(request, 'Recipe removed from favorites.')
    else:
        messages.success(request, 'Recipe added to favorites!')
    
    return redirect('recipes:recipe_detail', slug=slug)

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})

@login_required
def favorite_recipes(request):
    favorites = FavoriteRecipe.objects.filter(user=request.user).select_related('recipe')
    
    # Calculate highest rating
    highest_rating = 0
    for favorite in favorites:
        if favorite.recipe.average_rating and favorite.recipe.average_rating > highest_rating:
            highest_rating = favorite.recipe.average_rating
    
    context = {
        'favorites': favorites,
        'highest_rating': highest_rating,
    }
    return render(request, 'recipes/favorite_recipes.html', context)

@login_required
def category_list(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to manage categories.')
        return redirect('recipes:recipe_list')
        
    categories = Categories.objects.all().order_by('name')
    return render(request, 'recipes/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Categories, slug=slug)
    recipes = Recipe.objects.filter(category=category, is_published=True)
    return render(request, 'recipes/category_detail.html', {
        'category': category,
        'recipes': recipes
    })

@login_required
def category_create(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create categories.')
        return redirect('recipes:recipe_list')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('recipes:category_detail', slug=category.slug)
    else:
        form = CategoryForm()
    
    return render(request, 'recipes/category_form.html', {
        'form': form,
        'title': 'Create Category'
    })

# Profile Views
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('recipes:profile_detail', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'recipes/profile_form.html', {
        'form': form,
        'title': 'Edit Profile'
    })

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    if not user.profile.public_profile and request.user != user:
        messages.error(request, 'This profile is private.')
        return redirect('recipes:recipe_list')
    
    recipes = Recipe.objects.filter(author=user, is_published=True).order_by('-created_at')
    favorite_recipes = Recipe.objects.filter(favorites=user, is_published=True).order_by('-created_at')
    
    context = {
        'profile_user': user,
        'recipes': recipes,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'recipes/profile_detail.html', context)

@login_required
def dashboard(request):
    user = request.user
    recipes = Recipe.objects.filter(author=user).order_by('-created_at')
    favorite_recipes = Recipe.objects.filter(favorites=user).order_by('-created_at')
    recent_ratings = Rating.objects.filter(recipe__author=user).order_by('-created_at')[:5]
    recent_comments = Comment.objects.filter(recipe__author=user).order_by('-created_at')[:5]
    
    # Recipe statistics
    total_recipes = recipes.count()
    published_recipes = recipes.filter(is_published=True).count()
    total_favorites = user.favorite_recipes.count()
    total_ratings = Rating.objects.filter(recipe__author=user).count()
    
    context = {
        'recipes': recipes[:5],
        'favorite_recipes': favorite_recipes[:5],
        'recent_ratings': recent_ratings,
        'recent_comments': recent_comments,
        'stats': {
            'total_recipes': total_recipes,
            'published_recipes': published_recipes,
            'total_favorites': total_favorites,
            'total_ratings': total_ratings,
            'average_rating': user.profile.average_recipe_rating,
        }
    }
    return render(request, 'recipes/dashboard.html', context)

# Blog Views
def blog_list(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    categories = BlogCategories.objects.all()
    category_id = request.GET.get('category')
    
    if category_id:
        blog_posts = blog_posts.filter(category_id=category_id)

    subscription_form = SubscriptionForm()
    
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            messages.success(request, 'Thank you for subscribing!')
            subscription_form = SubscriptionForm()
    
    paginator = Paginator(blog_posts, 9)
    page = request.GET.get('page')
    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)
    
    context = {
        'blog_posts': blog_posts,
        'blog_categories': categories,
        'subscription_form': subscription_form,
        'current_category': category_id
    }
    
    return render(request, 'recipes/blog_list.html', context)

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('recipes:blog_list')
    else:
        form = BlogPostForm()
    
    categories = BlogCategories.objects.all()
    return render(request, 'recipes/blog_form.html', {
        'form': form,
        'categories': categories,
        'title': 'Create Blog Post'
    })

@login_required
def blog_update(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            form = BlogPostForm()
            return redirect('recipes:blog_list')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'recipes/blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        blog_post.delete()
        return redirect('recipes:blog_list')
    return render(request, 'recipes/blog_confirm_delete.html', {
        'blog_post': blog_post
    })

def blog_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'recipes/blog_detail.html', {
        'blog_post': blog_post
    })

def to_about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            form = ContactForm()
        else:
            # Add an error message for each form error
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ContactForm()
    
    return render(request, 'recipes/about.html', {'form': form})

def search_recipes(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(is_published=True)
    
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(instructions__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    paginator = Paginator(recipes, 9)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    context = {
        'recipes': recipes,
        'query': query,
        'total_results': recipes.paginator.count if query else None,
    }
    return render(request, 'recipes/search_results.html', context)