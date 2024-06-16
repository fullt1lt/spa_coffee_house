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

from myspa.models import MassageTherapist, Review, SpaUser, TypeCategories, SpaСategories
from spa.mixins import SuperUserRequiredMixin

class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('new_index')
        else:
            return reverse_lazy('new_index')
        
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
    template_name = 'new_index.html'

    def get(self, request, *args, **kwargs):
        spa_categories = SpaСategories.objects.all().order_by('name')
        massage_therapists = MassageTherapist.objects.all().order_by('-average_rating')
        review_form = ReviewForm()
        reviews = Review.objects.all().order_by('-created_at')
        
        paginator = Paginator(reviews, 4)
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


class HomePage(ListView):
    template_name = 'index.html'
    queryset = SpaСategories.objects.all()
    ordering = ['name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['massage_therapist'] = MassageTherapist.objects.all()
        return context


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
        return context
    
    def get_queryset(self):
        return TypeCategories.objects.filter(categories__id=self.kwargs['pk'])
    