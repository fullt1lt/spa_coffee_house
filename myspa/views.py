from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import login, authenticate
from forms.forms import CategoriesAddForm, CategoriesUpdateForm, LoginUserForm, MassageTherapistForm, RegisterUserForm, ReviewForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from myspa.models import BlogAndNews, CafeProduct, Gallery, MassageTherapist, Review, SpaUser, TypeBlogAndNews, TypeCafeProduct, TypeCategories, TypeGallery, SpaСategories
from spa.mixins import SuperUserRequiredMixin

        
class Register(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = '/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return response
    

class MainPage(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        spa_categories = SpaСategories.objects.all().order_by('name')
        massage_therapists = MassageTherapist.objects.all().order_by('-average_rating')
        review_form = ReviewForm()
        reviews = Review.objects.all().order_by('-created_at')

        paginator = Paginator(reviews, 2)
        page_number = request.GET.get('page')
        page_reviews = paginator.get_page(page_number)

        context = {
            'spa_categories': spa_categories,
            'massage_therapists': massage_therapists,
            'review_form': review_form,
            'reviews': page_reviews,
            'form': LoginUserForm(),
            'register_form': RegisterUserForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'register' in request.POST:
            return self.handle_register(request)
        elif 'login' in request.POST:
            return self.handle_login(request)
        elif 'therapist' in request.POST:
            return self.handle_review(request)
        return self.get(request, *args, **kwargs)

    def handle_register(self, request):
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.username = user.email
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
            return redirect('/')
        # Передача формы с ошибками в контекст для вывода ошибок в шаблоне
        context = {
            'register_form': register_form,
            'form': LoginUserForm(),
            'review_form': ReviewForm(),
            'spa_categories': SpaСategories.objects.all().order_by('name'),
            'massage_therapists': MassageTherapist.objects.all().order_by('-average_rating'),
            'reviews': Review.objects.select_related('user').all().order_by('-created_at'),
        }
        return render(request, self.template_name, context)

    def handle_login(self, request):
        login_form = LoginUserForm(data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Указываем бэкенд явно
                return redirect('/')
        # Передача формы с ошибками в контекст для вывода ошибок в шаблоне
        context = {
            'register_form': RegisterUserForm(),
            'form': login_form,
            'review_form': ReviewForm(),
            'spa_categories': SpaСategories.objects.all().order_by('name'),
            'massage_therapists': MassageTherapist.objects.all().order_by('-average_rating'),
            'reviews': Review.objects.select_related('user').all().order_by('-created_at'),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def handle_review(self, request):
        therapist_id = request.POST.get('therapist')
        therapist = get_object_or_404(MassageTherapist, id=therapist_id)
        review_form = ReviewForm(request.POST)
        
        if review_form.is_valid():
            rating = review_form.cleaned_data['rating']
            comment = review_form.cleaned_data['comment']
            review = Review.objects.create(
                therapist=therapist,
                user=request.user,
                rating=rating,
                comment=comment
            )
            review.save()
            return redirect('/')
        
        # Передача формы с ошибками в контекст для вывода ошибок в шаблоне
        context = {
            'register_form': RegisterUserForm(),
            'form': LoginUserForm(),
            'review_form': review_form,
            'spa_categories': SpaСategories.objects.all().order_by('name'),
            'massage_therapists': MassageTherapist.objects.all().order_by('-average_rating'),
            'reviews': Review.objects.select_related('user').all().order_by('-created_at'),
        }
        return render(request, self.template_name, context)


class AdminMainPage(SuperUserRequiredMixin, View):
    template_name = 'index_admin.html'

    def get_context_data(self, **kwargs):
        context = {
            'register_form': RegisterUserForm(),
            'form': LoginUserForm(),
            'review_form': ReviewForm(),
            'spa_categories': SpaСategories.objects.all().order_by('name'),
            'massage_therapists': MassageTherapist.objects.all().order_by('-average_rating'),
            'reviews': Review.objects.select_related('user').all().order_by('-created_at'),
            'categories_update_form': CategoriesUpdateForm(),
            'categories_add_form': CategoriesAddForm(),
        }
        context.update(kwargs)
        return context

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.get_context_data()['reviews'], 2)
        page_number = request.GET.get('page')
        page_reviews = paginator.get_page(page_number)
        
        context = self.get_context_data(reviews=page_reviews)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'register' in request.POST:
            return self.handle_register(request)
        elif 'login' in request.POST:
            return self.handle_login(request)
        elif 'therapist' in request.POST:
            return self.handle_review(request)
        elif 'update_categories' in request.POST:
            category_id = request.POST.get('category_id')
            return self.update_categories(request, category_id)
        elif 'add_categories' in request.POST:
            return self.add_categories(request)
        return self.get(request, *args, **kwargs)

    def handle_register(self, request):
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.username = user.email
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        context = self.get_context_data(register_form=register_form)
        return render(request, self.template_name, context)

    def handle_login(self, request):
        login_form = LoginUserForm(data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
        context = self.get_context_data(form=login_form)
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def handle_review(self, request):
        therapist_id = request.POST.get('therapist')
        therapist = get_object_or_404(MassageTherapist, id=therapist_id)
        review_form = ReviewForm(request.POST)
        
        if review_form.is_valid():
            rating = review_form.cleaned_data['rating']
            comment = review_form.cleaned_data['comment']
            review = Review.objects.create(
                therapist=therapist,
                user=request.user,
                rating=rating,
                comment=comment
            )
            review.save()
            return redirect('/')
        
        context = self.get_context_data(review_form=review_form)
        return render(request, self.template_name, context)

    def update_categories(self, request, category_id):
        category = get_object_or_404(SpaСategories, id=category_id)
        categories_update_form = CategoriesUpdateForm(data=request.POST, files=request.FILES, instance=category)
        if categories_update_form.is_valid():
            categories_update_form.save()
            return redirect('/main/')
        
        context = self.get_context_data(categories_update_form=categories_update_form)
        return render(request, self.template_name, context)

    def add_categories(self, request):
        categories_add_form = CategoriesAddForm(request.POST, request.FILES)
        if categories_add_form.is_valid():
            categories_add_form.save()
            return redirect('/main/')
        
        context = self.get_context_data(categories_add_form=categories_add_form)
        return render(request, self.template_name, context) 
        

@method_decorator(csrf_exempt, name='dispatch')
class GetReviews(View):

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        reviews = Review.objects.all().order_by('-created_at')
        paginator = Paginator(reviews, 2)
        page_reviews = paginator.get_page(page)
        
        reviews_list = [{
            'id': review.id,
            'name': review.user.first_name,
            'surname': review.user.last_name,
            'comment': review.comment,
            'rating': review.rating,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'profile_image': review.user.profile_image.url if review.user.profile_image else None
        } for review in page_reviews]
        
        return JsonResponse({'reviews': reviews_list, 'has_next': page_reviews.has_next()})

class DeleteSpaCategoriesView(SuperUserRequiredMixin, DeleteView):
    model = SpaСategories
    success_url = '/main/'

class CreateMassageTherapistView(SuperUserRequiredMixin, CreateView):
    model = MassageTherapist
    fields = ['salon']
    template_name = 'create_massage_therapist.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        user_form = RegisterUserForm()
        therapist_form = MassageTherapistForm()
        return self.render_to_response({'user_form': user_form, 'therapist_form': therapist_form})

    def post(self, request, *args, **kwargs):
        user_form = RegisterUserForm(request.POST, request.FILES)
        therapist_form = MassageTherapistForm(request.POST)
        
        if user_form.is_valid() and therapist_form.is_valid():
            user = user_form.save()
            therapist = therapist_form.save(commit=False)
            therapist.user = user
            therapist.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(self.success_url)

        return self.render_to_response({'user_form': user_form, 'therapist_form': therapist_form})
    

class TypeCategoriesListView(ListView):
    model = TypeCategories
    ordering = ['name']
    template_name = 'categories.html'
    context_object_name = 'type_categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['another_model_list'] = SpaСategories.objects.all().order_by('name')
        context['category_pk'] = self.kwargs['pk']

        type_categories = self.get_queryset()

        type_categories_data = []
        for type_category in type_categories:
            sessions = type_category.sessions.all()
            durations = "/".join([str(int(session.duration.total_seconds() // 60)) for session in sessions])
            prices = "/".join([str(int(session.price)) for session in sessions])
            type_categories_data.append({
                'type_category': type_category,
                'durations': durations,
                'prices': prices,
            })

        context['type_categories_data'] = type_categories_data
        return context
    
    def get_queryset(self):
        return TypeCategories.objects.filter(categories__id=self.kwargs['pk']).prefetch_related('sessions')
    

class CafeView(ListView):
    model = CafeProduct
    queryset = TypeCafeProduct.objects.all().order_by('name')
    ordering = ['name']
    template_name = 'cafe_index.html'
    context_object_name = "type_cafe_product"


class CafeTypeProductListView(ListView):
    model = CafeProduct
    ordering = ['name']
    template_name = 'cafe_categories.html'
    context_object_name = 'type_product_categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_cafe_product'] = TypeCafeProduct.objects.all().order_by('name')
        context['category_pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return CafeProduct.objects.filter(type_cafe_product=self.kwargs['pk'])
    

class BlogNewsView(ListView):
    model = BlogAndNews
    queryset = TypeBlogAndNews.objects.all().order_by('name')
    ordering = ['name']
    template_name = 'blog_news.html'
    context_object_name = "type_blog_news"
    

class TypeBlogNewsViewListView(ListView):
    model = BlogAndNews
    paginate_by = 2
    ordering = ['name']
    template_name = 'blog_news_categories.html'
    context_object_name = 'type_blog_news_categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_blog_news'] = TypeBlogAndNews.objects.all().order_by('name')
        context['category_pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return BlogAndNews.objects.filter(type_blog_and_news=self.kwargs['pk'])
    
    
class GalleryView(ListView):
    model = TypeGallery
    ordering = ['name']
    template_name = 'gallery.html'
    context_object_name = 'type_gallery'


class TypeGalleryListView(ListView):
    model = Gallery
    paginate_by = 3
    ordering = ['name']
    template_name = 'gallery_categories.html'
    context_object_name = 'type_gallery_categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_gallery'] = TypeGallery.objects.all().order_by('name')
        context['category_pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return Gallery.objects.filter(type_gallery=self.kwargs['pk'])