from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import login
from forms.forms import LoginUserForm, MassageTherapistForm, RegisterUserForm, ReviewForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator

from myspa.models import BlogAndNews, CafeProduct, MassageTherapist, Review, SpaUser, TypeBlogAndNews, TypeCafeProduct, TypeCategories, SpaСategories
from spa.mixins import SuperUserRequiredMixin

class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('index')
        else:
            return reverse_lazy('index')
        
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
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        therapist_id = request.POST.get('therapist')
        therapist = get_object_or_404(MassageTherapist, id=therapist_id)
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            review = Review.objects.create(
                therapist=therapist,
                user=request.user,
                rating=rating,
                comment=comment
            )
            review.save()
            return redirect('/')

        spa_categories = SpaСategories.objects.all()
        massage_therapists = MassageTherapist.objects.all()
        context = {
            'spa_categories': spa_categories,
            'massage_therapists': massage_therapists,
            'review_form': form,
        }
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
            'user': review.user.username,
            'comment': review.comment,
            'rating': review.rating,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'profile_image': review.user.profile_image.url if review.user.profile_image else None
        } for review in page_reviews]
        
        return JsonResponse({'reviews': reviews_list, 'has_next': page_reviews.has_next()})


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