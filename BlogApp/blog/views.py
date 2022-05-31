from .forms import PostForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib import messages
from .models import Post, Profile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'blog/account/dashboard.html', {'section': 'dashboard'})

@login_required
def user_profile(request):
    return render(request, 'blog/account/user_profile.html')

@login_required
def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.INFO, 'Профиль успешно обновлен')
            return redirect('user_edit')
        else:
            messages.add_message(request, messages.WARNING, 'Ошибка при обновлении вашего профиля')
            return redirect('user_edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
            'blog/account/user_edit.html',
            {'user_form': user_form,
            'profile_form': profile_form})

def register(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the User object
                new_user.save()
                profile = Profile.objects.create(user=new_user)
                return render(request, 'blog/account/register_done.html', {'new_user': new_user})
        else:
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/account/register.html', {'user_form': user_form})

def post_detail(request, year, month, day):
    post = get_object_or_404(Post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(request,'blog/post/detail.html', {'post': post})

def get_absolute_url(self):
        return reverse('blog:post_detail',
            args=[self.publish.year,
                  self.publish.strftime('%m'),
                  self.publish.strftime('%d'),
                  self.slug])

def delete(request, id):
    if request.user.is_authenticated:
        try:
            if request.method == "GET":
                post = Post.objects.get(id=id)
                post.delete()
                return redirect('home')
        except Exception as e:
            print(e)
            return render(request, 'blog/post/delete.html')
    else:
        return redirect('home')

def edit(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        if request.user == post.author:
            try:
                if request.method == "POST":
                    post.title = request.POST.get("title")
                    post.body = request.POST.get("body")
                    post.save()
                    return redirect('home')
                else:
                    return render(request, 'blog/post/edit.html', {"post": post})
            except Post.DoesNotExist:
                return render('blog/post/edit.html')
        else: 
            return redirect('home')
    else:
        return redirect('home')

def create(request):
    if request.user.is_authenticated:
        error = ''
        if request.method == 'POST':
            form = PostForm(request.POST)
            print(form)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                form.save()
                return redirect('home')
            else:
                error = 'Форма заполнена неверно'
        form = PostForm()
        return render(request, 'blog/post/create.html', {'form': form})
    else:
        return redirect('home')

def about(request):
    return render(request, 'blog/about.html')

def handler404(request, exception=None):
    return HttpResponseRedirect("/")

def handler500(request, exception=None):
    return HttpResponseRedirect('/')


class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
