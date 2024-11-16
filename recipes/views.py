from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, Rating, Comment, BlogPost, Categories, BlogCategories
from .forms import RecipeForm, RatingForm, CommentForm, BlogPostForm, SubscriptionForm, ContactForm
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    recipes_greater_than_3 = Recipe.objects.filter(ratings__rating__gt=3).distinct().order_by('-created_at') 
    ratings = Rating.objects.filter(recipe__in=recipes_greater_than_3)
    comments = Comment.objects.filter(recipe__in=recipes_greater_than_3)
    
    # Calculate avaerage rating for each recipe
    recipes_with_avg_rating_and_comments = []
    for recipe in recipes_greater_than_3:
        avg_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'))['rating__avg'] or 0
        comment_count = Comment.objects.filter(recipe=recipe).count()
        recipe.average_rating = round(avg_rating)
        recipe.comment_count = comment_count
        recipes_with_avg_rating_and_comments.append(recipe)
    
    subscription_form = SubscriptionForm()
    
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription_form.save()
            return redirect('recipes:recipe_list')
        
    return render(request, 'recipes/recipe_list.html', {
        'recipes_with_avg_rating_and_comments': recipes_with_avg_rating_and_comments, 
        'recipes': recipes, 
        'ratings': ratings, 
        'comments': comments,
        'subscription_form': subscription_form,
        })

def recipes_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    ratings = Rating.objects.filter(recipe__in=recipes)
    comments = Comment.objects.filter(recipe__in=recipes)
    
    # Handle search query
    query = request.GET.get('q')
    if query:
        recipes = recipes.filter(title__icontains=query)
        
    # Handle category selection
    category_id = request.GET.get('category')
    if category_id:
        recipes = recipes.filter(category_id=category_id)
    
    # Calculate avaerage rating for each recipe
    recipes_with_avg_rating_and_comments = []
    for recipe in recipes:
        avg_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'))['rating__avg'] or 0
        comment_count = Comment.objects.filter(recipe=recipe).count()
        recipe.average_rating = round(avg_rating)
        recipe.comment_count = comment_count
        recipes_with_avg_rating_and_comments.append(recipe)
    
    # Paginate the recipes
    paginator = Paginator(recipes_with_avg_rating_and_comments, 9)
    page = request.GET.get('page')
    try:
        recipes_with_avg_rating_and_comments = paginator.page(page)
    except PageNotAnInteger:
        recipes_with_avg_rating_and_comments = paginator.page(1)
    except EmptyPage:
        recipes_with_avg_rating_and_comments = paginator.page(paginator.num_pages)
        
    categories = Categories.objects.all()
    
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes_with_avg_rating_and_comments, 'ratings': ratings, 'comments': comments, 'categories': categories, 'query': query, 'selected_category': category_id,})

        
def search_recipes(request):
    recipes_search = Recipe.objects.all().order_by('-created_at')
    query_search = request.GET.get('q')
    if query_search:
        recipes_search = Recipe.objects.filter(title__icontains=query_search)
    else:
        recipes_search = Recipe.objects.none()
    
    # Calculate avaerage rating for each recipe
    recipes_with_avg_rating_and_comments = []
    for recipe in recipes_search:
        avg_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'))['rating__avg'] or 0
        comment_count = Comment.objects.filter(recipe=recipe).count()
        recipe.average_rating = round(avg_rating)
        recipe.comment_count = comment_count
        recipes_with_avg_rating_and_comments.append(recipe)
        
    
    # Paginate the recipes
    paginator = Paginator(recipes_with_avg_rating_and_comments, 9)
    page = request.GET.get('page')
    try:
        recipes_with_avg_rating_and_comments = paginator.page(page)
    except PageNotAnInteger:
        recipes_with_avg_rating_and_comments = paginator.page(1)
    except EmptyPage:
        recipes_with_avg_rating_and_comments = paginator.page(paginator.num_pages)
    
    return render(request, 'recipes/recipes_list.html', {
        'recipes_search': recipes_with_avg_rating_and_comments,
        'query_search': query_search,
    })

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form = RecipeForm()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form,})

@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            form = RecipeForm()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form,})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipes:recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ratings = round(recipe.ratings.aggregate(Avg('rating'))['rating__avg'] or 0)
    comments = recipe.comments.all()
    rating_form = RatingForm(prefix='rating_form')
    comment_form = CommentForm(prefix='comment_form')
    
    avg_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'))['rating__avg'] or 0
    comment_count = Comment.objects.filter(recipe=recipe).count()
    recipe.average_rating = round(avg_rating)
    recipe.comment_count = comment_count
    
    if request.method == 'POST':
        rating_form = RatingForm(request.POST, prefix='rating_form')
        comment_form = CommentForm(request.POST, prefix='comment_form')
        
        if rating_form.is_valid() and comment_form.is_valid():
            # Save the rating
            rating = rating_form.save(commit=False)
            rating.recipe = recipe
            rating.user = request.user
            rating.save()
            
            # Save the comment
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            
            return redirect('recipes:recipe_detail', pk=pk)
        else:
            # If only one form is valid, re-render the page with errors
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.recipe = recipe
                rating.user = request.user
                rating.save()
            elif comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.save()
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ratings': ratings,
        'comments': comments,
        'rating_form': rating_form,
        'comment_form': comment_form,
    })
    

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
    
    return render(request, 'recipes/blog_list.html', { 'blog_posts': blog_posts, 'categories': categories })

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            form = BlogPostForm()
            return redirect('recipes:blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'recipes/blog_form.html', {'form': form})


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