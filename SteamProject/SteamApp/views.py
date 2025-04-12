from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Game
from .forms import RegisterForm, LoginForm, PostGameForm, EditAccountForm, ChangePasswordForm
from django.contrib import messages

def home_view(request):
    games = Game.objects.all().order_by('-created_at')  # Newest games first
    return render(request, 'app/home.html', {'games': games})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                
                if not remember_me:
                    # Set session to expire when browser closes
                    request.session.set_expiry(0)
                
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

@login_required
def dashboard_view(request):
    game= Game.objects.filter(publisher=request.user).first()
    is_d= False
    
    if game is not None:
        is_d = True
    
    user_games = Game.objects.filter(publisher=request.user).order_by('-created_at')
    return render(request, 'auth/dashboard.html', {'user':request.user, 'is_d': is_d, 'games': user_games}) 

@login_required
def post_game_view(request):
    if request.method == 'POST':
        form = PostGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.publisher = request.user  # Set the publisher to current user
            game.save()
            messages.success(request, 'Game posted successfully!')
            return redirect('home')
    else:
        form = PostGameForm()
    return render(request, 'games/post_game.html', {'form': form})

@login_required
def edit_game_view(request, id:int):
    game = Game.objects.filter(id=id).first()
    
    # Check if game exists
    if not game:
        messages.error(request, 'Game not found!')
        return redirect('home')
    
    # Verify ownership
    if game.publisher != request.user:
        messages.error(request, 'You are not the publisher of this game!')
        return redirect('home')
    
    if request.method == "POST":
        form = PostGameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game updated successfully!')
            return redirect('dashboard')
    else:
        form = PostGameForm(instance=game)
    
    return render(request, 'games/post_game.html', {'form': form, 'editing': True, 'game': game})

@login_required
def delete_game(request, id):  # Added id parameter
    game = get_object_or_404(Game, id=id)
    
    # Verify ownership
    if game.publisher != request.user:
        messages.error(request, 'You are not authorized to delete this game!')
        return redirect('my_games')
    
    if request.method == "POST":
        game_name = game.name
        game.delete()
        messages.success(request, f'Game "{game_name}" was deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'games/delete_game.html', {'game': game})  # Pass game to template

@login_required
def continue_warning(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'POST':
        # Update metrics only if user clicks "Continue"
        game.visited += 1
        
        # Calculate revenue (assuming 30% platform cut)
        platform_cut = Decimal('0.3')
        revenue = game.price * (Decimal('1') - platform_cut)
        game.revenue += revenue
        
        game.save()
        return redirect(game.link)
    
    context = {
        'game': game,
        'estimated_revenue': game.price * Decimal('0.7')  # Show estimated revenue
    }
    return render(request, 'games/continue.html', context)

@login_required
def edit_user_view(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('dashboard')  # Moved inside if valid
    else:
        form = EditAccountForm(instance=request.user)
    
    return render(request, 'auth/edit.html', {
        'form': form,
        'email': request.user.email
    })

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important: updates the session to prevent logout
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'auth/change_password.html', {
        'form': form
    })

""" # This thing was implimented in 'dashboard' view
@login_required
def my_games_view(request):
    user_games = Game.objects.filter(publisher=request.user).order_by('-created_at')
    return render(request, 'games/my_games.html', {'games': user_games})
"""