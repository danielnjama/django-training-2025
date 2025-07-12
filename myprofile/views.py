from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# from . models import UserProfile
from django.contrib.auth.views import PasswordResetView
from .models import Blog, Comment, Category, Tag
from django.db.models import Count
from django.core.mail import send_mail
from django.http import JsonResponse
# from .forms import CustomPasswordResetForm





# class CustomPasswordResetView(PasswordResetView):
#     form_class = CustomPasswordResetForm
#     template_name = 'registration/password_reset_form.html'  # or your custom path




def about(request):
    return render(request,'about.html')



# def blog(request):
#     return render(request,'blog.html')

# def blog(request):
#     blogs = Blog.objects.all().order_by('-created_at')
#     categories = Category.objects.annotate(blog_count=Count('blog'))
#     return render(request,'blog.html',{'blogs': blogs,  'categories': categories})


def blog(request):
    category_slug = request.GET.get('category')  # from URL query parameter
    tag_url = request.GET.get('tag')

    categories = Category.objects.annotate(blog_count=Count('blog'))
    tags = Tag.objects.all()

    if category_slug:
        category = get_object_or_404(Category, url=category_slug)
        blogs = Blog.objects.filter(category=category).order_by('-created_at')
    elif tag_url:
        tag = get_object_or_404(Tag, url=tag_url)
        blogs = Blog.objects.filter(tags=tag).order_by('-created_at')
    else:
        category = None
        blogs = Blog.objects.all().order_by('-created_at')

    return render(request, 'blog.html', {
        'blogs': blogs,
        'categories': categories,
        # 'selected_category': category,
        'tags':tags
    })




def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = blog.comments.filter(approved=True)
    categories = Category.objects.annotate(blog_count=Count('blog'))
    blogs = Blog.objects.all().order_by('-created_at')

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        comment = Comment(name=name, email=email, message=message, blog=blog)
        comment.save()

    return render(request, 'single-blog.html', {
        'blog': blog,
        'comments': comments,
        'categories':categories,
        'blogs':blogs

        
    })


def contact(request):
    if request.method =='POST':
        name = request.POST.get('name')
        sender = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')

        # send_mail(subject=subject,message=message,from_email=sender,recipient_list=['admin@dtechnologys.com',],fail_silently=False)
        try:
            send_mail(subject=subject,message=message,from_email=sender,recipient_list=['admin@dtechnologys.com',],fail_silently=False)
            return JsonResponse({'status': 'Success', 'message': 'Email sent!'}) 
        except:
            return JsonResponse({'status': 'Error', 'message': 'Email Not sent!'}) 
    return render(request,'contact.html')

def index(request):
    return render(request,'index.html')

def portfolio(request):
    return render(request,'portfolio.html')





def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        phone = request.POST.get('phone', '')

        errors = []

        # Check if passwords match
        if password != password2:
            errors.append("Passwords do not match!")
        
        #Password validation
        try:
            validate_password(password)
        except ValidationError as e:
            errors.append(" ".join(e.messages))
            # return render(request, 'register.html')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            errors.append("Username is already taken!")

        # Check if email exists
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered!")
        
        #validate phone number
        if len(phone) > 10 and len(phone) < 15:
            try:
                phone = int(phone)
            except:
                errors.append("Invalid Phone Number!")
        else:
            errors.append("Invalid Phone Number")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html', {'first_name': first_name,'last_name': last_name, 'username': username, 'email': email,'phone':phone})

        # Create user
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, is_staff=True)

        #save phone number
        UserProfile.objects.create(user=user,phone_number=phone)
        
        #Add user to group
        group, created = Group.objects.get_or_create(name="Staff user")
        user.groups.add(group)
        messages.success(request, "User created successfully! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')



def logout(request):
    auth.logout(request)
    return redirect("login")