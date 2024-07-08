from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import login, authenticate
from forms.forms import AddCafeProductForm, AddGalleryForm, AddTypeCafeProductForm, CafeProductForm, CategoriesAddForm, CategoriesUpdateForm, LoginUserForm, MassageTherapistForm, MassageTherapistUpdateForm, ProcedureAddForm, ProcedureEditForm, ProcedureForm, RegisterUserForm, ReviewForm, ScheduleForm, TherapistForm, TypeCategoryCustomForm, TypeCategoryForm, UpdateTypeCafeProductForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from myspa.models import BlogAndNews, CafeProduct, Gallery, MassageTherapist, Position, Procedure, Record, Review, Schedule, SpaUser, TypeBlogAndNews, TypeCafeProduct, TypeCategories, TypeGallery, SpaСategories
from myspa.units import SlotsValidator
from spa.mixins import SuperUserRequiredMixin
from django.utils.dateparse import parse_date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

        
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
    success_url = '/admin-main-page/'
    

class DeleteTherapistView(SuperUserRequiredMixin, DeleteView):
    model = MassageTherapist
    success_url = '/admin-main-page/'
    

class DeleteTypeCategoriesView(SuperUserRequiredMixin, DeleteView):
    model = TypeCategories
    success_url = '/admin-main-page/'
    
    
class DeleteProcedureView(SuperUserRequiredMixin, DeleteView):
    model = Procedure
    success_url = '/admin-main-page/'
    

class DeleteCafeProductView(SuperUserRequiredMixin, DeleteView):
    model = CafeProduct
    success_url = '/admin-main-page/'
    
class DeleteTypeCafeProductView(SuperUserRequiredMixin, DeleteView):
    model = TypeCafeProduct
    success_url = '/admin-main-page/'
    
class DeleteGalleryView(SuperUserRequiredMixin, DeleteView):
    model = Gallery
    success_url = '/admin-main-page/'


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
    

def get_therapist_schedule(request, therapist_id):
    therapist = get_object_or_404(MassageTherapist, id=therapist_id)
    today = timezone.now().date()
    schedules = Schedule.objects.filter(therapist=therapist, day__gte=today).order_by('day', 'start_time')
    schedule_data = []

    for schedule in schedules:
        records = Record.objects.filter(schedule=schedule).order_by('start_time')
        records_data = []

        for record in records:
            start_time = record.start_time
            duration = record.procedure.duration
            end_time = (make_aware(datetime.combine(schedule.day, start_time)) + duration).time()
            records_data.append({
                'start_time': start_time.strftime('%H:%M'),
                'end_time': end_time.strftime('%H:%M'),
                'procedure_name': record.procedure.type_category.name,
                'client_first_name': record.client.first_name if record.client else 'N/A',
                'client_last_name': record.client.last_name if record.client else 'N/A',
            })

        schedule_data.append({
            'day': schedule.day.strftime('%Y-%m-%d'),
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
            'records': records_data,
        })

    return JsonResponse({'schedules': schedule_data})


class AdminMainPage(SuperUserRequiredMixin, View):
    template_name = 'admin_page.html'

    def get_context_data(self, **kwargs):
        context = {
            'register_form': RegisterUserForm(),
            'spa_categories': SpaСategories.objects.all().order_by('name'),
            'massage_therapists': MassageTherapist.objects.all().order_by('-average_rating'),
            'categories_update_form': CategoriesUpdateForm(),
            'categories_add_form': CategoriesAddForm(),
            'therapist_update_form': MassageTherapistUpdateForm(),
            'all_positions': Position.objects.all(),
            'therapist_form': MassageTherapistForm(),
            'schedule_form': kwargs.get('schedule_form', ScheduleForm()),
            'therapists_with_schedule': MassageTherapist.objects.filter(schedule__isnull=False).distinct(),
            'type_category_form': kwargs.get('type_category_form', TypeCategoryForm()),
            'type_costom_category_form': kwargs.get('type_costom_category_form', TypeCategoryCustomForm()),
            'procedure_form': kwargs.get('procedure_form', ProcedureEditForm()),
            'procedures': Procedure.objects.select_related('type_category__categories').order_by('type_category__categories', 'type_category', 'duration'),
            'procedure_add_form': kwargs.get('procedure_add_form', ProcedureAddForm()),
            'cafe_product_form': kwargs.get('cafe_product_form', CafeProductForm()),
            'add_cafe_product_form': kwargs.get('add_cafe_product_form', AddCafeProductForm()),
            'cafe_products': CafeProduct.objects.all().order_by('type_cafe_product'),
            'type_cafe_product_form': kwargs.get('type_cafe_product_form', UpdateTypeCafeProductForm()),
            'add_type_cafe_product_form': kwargs.get('add_type_cafe_product_form', AddTypeCafeProductForm()),
            'type_cafe_products': TypeCafeProduct.objects.all(),
            'add_gallery_form': AddGalleryForm(),
            'galleries': Gallery.objects.all().order_by('type_gallery'),
        }
        context.update(kwargs)
        context.update(self.get_type_categories_data())
        return context

    def get_type_categories_data(self):
        type_categories = TypeCategories.objects.prefetch_related('sessions').all()

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

        return {'type_categories_data': type_categories_data}

    def get(self, request, *args, **kwargs):  
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'update_categories' in request.POST:
            category_id = request.POST.get('category_id')
            return self.update_categories(request, category_id)
        elif 'add_categories' in request.POST:
            return self.add_categories(request)
        elif 'update_therapist' in request.POST:
            therapist_id = request.POST.get('therapist_id')
            return self.update_therapist(request, therapist_id)
        elif 'add_therapist' in request.POST:
            return self.add_therapist(request)
        elif 'schedule' in request.POST:
            return self.handle_schedule(request)
        elif 'update_type_category' in request.POST:
            type_category_id = request.POST.get('type_category_id')
            return self.update_type_category(request, type_category_id)
        elif 'add_type_category' in request.POST:
            return self.add_type_category(request)
        elif 'update_procedure' in request.POST:
            procedure_id = request.POST.get('procedure_id')
            return self.update_procedure(request, procedure_id)
        elif 'add_procedure' in request.POST:
            return self.add_procedure(request)
        elif 'add_cafe_product' in request.POST:
            return self.add_cafe_product(request)
        elif 'update_cafe_product' in request.POST:
            cafe_product_id = request.POST.get('cafe_product_id')
            return self.update_cafe_product(request, cafe_product_id)
        elif 'add_type_cafe_product' in request.POST:
            return self.add_type_cafe_product(request)
        elif 'update_type_cafe_product' in request.POST:
            type_cafe_product_id = request.POST.get('type_cafe_product_id')
            return self.update_type_cafe_product(request, type_cafe_product_id)
        elif 'add_gallery' in request.POST:
            return self.add_gallery(request)
        return self.get(request, *args, **kwargs)


    def update_categories(self, request, category_id):
        category = get_object_or_404(SpaСategories, id=category_id)
        categories_update_form = CategoriesUpdateForm(data=request.POST, files=request.FILES, instance=category)
        if categories_update_form.is_valid():
            categories_update_form.save()
            return redirect('/admin-main-page/')
        
        context = self.get_context_data(categories_update_form=categories_update_form)
        return render(request, self.template_name, context)

    def add_categories(self, request):
        categories_add_form = CategoriesAddForm(request.POST, request.FILES)
        if categories_add_form.is_valid():
            categories_add_form.save()
            return redirect('/admin-main-page/')
        
        context = self.get_context_data(categories_add_form=categories_add_form)
        return render(request, self.template_name, context) 
        
    def update_therapist(self, request, therapist_id):
        therapist = get_object_or_404(MassageTherapist, id=therapist_id)
        form = MassageTherapistUpdateForm(request.POST, request.FILES, instance=therapist)
        if form.is_valid():
            user = therapist.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if 'profile_image' in form.cleaned_data and form.cleaned_data['profile_image']:
                user.profile_image = form.cleaned_data['profile_image']
            user.save()
            therapist.position.set(form.cleaned_data['position'])
            therapist.save()
            return redirect('/admin-main-page/')

        context = self.get_context_data()
        context['therapist_update_form'] = form
        return render(request, self.template_name, context)
    
    def add_therapist(self, request, *args, **kwargs):
        register_form = RegisterUserForm(request.POST, request.FILES)
        therapist_form = MassageTherapistForm(request.POST)

        if register_form.is_valid() and therapist_form.is_valid():
            try:
                user = register_form.save(commit=False)
                user.username = user.email
                if 'profile_image' in register_form.cleaned_data and register_form.cleaned_data['profile_image']:
                    user.profile_image = register_form.cleaned_data['profile_image']
                user.save()
                therapist = therapist_form.save(commit=False)
                therapist.user = user
                therapist.save()
                therapist.position.set(therapist_form.cleaned_data['position'])
                return redirect('/admin-main-page/')
            except IntegrityError:
                register_form.add_error(None, 'Пользователь с таким именем уже существует.')

        context = self.get_context_data()
        context['register_form'] = register_form
        context['therapist_form'] = therapist_form
        return render(request, self.template_name, context)

    def handle_schedule(self, request):
        form = ScheduleForm(request.POST)
        if form.is_valid():
            dates = form.cleaned_data['dates'].split(',')
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            therapist = form.cleaned_data['therapist']
    
            # Проверка времени
            min_time = datetime.strptime("08:00", '%H:%M').time()
            max_time = datetime.strptime("22:00", '%H:%M').time()
            if start_time < min_time or end_time > max_time:
                form.add_error(None, "Час повинен бути в межах від 08:00 до 22:00.")
            elif start_time >= end_time:
                form.add_error(None, "Час кінця роботи повинен бути більшим за час початку роботи.")
            else:
                unavailable_dates = []
                for date in dates:
                    day = parse_date(date)
                    if Schedule.objects.filter(therapist=therapist, day=day).exists():
                        unavailable_dates.append(date)
                    else:
                        Schedule.objects.create(
                            therapist=therapist,
                            day=day,
                            start_time=start_time,
                            end_time=end_time
                        )
    
                if unavailable_dates:
                    form.add_error(None, f"Уже є розклад на такі дати {', '.join(unavailable_dates)}")
                    return self.render_to_response(self.get_context_data(schedule_form=form))
    
                return redirect('/admin-main-page/')
        return self.render_to_response(self.get_context_data(schedule_form=form))

    def update_type_category(self, request, type_category_id):
        type_category = get_object_or_404(TypeCategories, id=type_category_id)
        type_category_update_form = TypeCategoryForm(data=request.POST, files=request.FILES, instance=type_category)
        if type_category_update_form.is_valid():
            type_category_update_form.save()
            return redirect('/admin-main-page/')

        context = self.get_context_data(type_category_update_form=type_category_update_form)
        return render(request, self.template_name, context)

    def add_type_category(self, request):
        if request.method == 'POST':
            type_category_form = TypeCategoryCustomForm(request.POST, request.FILES)
            if type_category_form.is_valid():
                type_category_form.save()
                return redirect('/admin-main-page/')
            else:
                print("Файл не загружен или невалиден:", type_category_form.errors)

        context = self.get_context_data(type_category_form=type_category_form)
        return render(request, self.template_name, context)
    
    def update_procedure(self, request, procedure_id):
        procedure = get_object_or_404(Procedure, id=procedure_id)
        procedure_form = ProcedureEditForm(data=request.POST, instance=procedure)
        if procedure_form.is_valid():
            procedure_form.save()
            return redirect('/admin-main-page/')

        context = self.get_context_data(procedure_form=procedure_form)
        return render(request, self.template_name, context)
    
    def add_procedure(self, request):
        procedure_add_form = ProcedureAddForm(request.POST)
        if procedure_add_form.is_valid():
            procedure_add_form.save()
            return redirect('/admin-main-page/')

        context = self.get_context_data(procedure_add_form=procedure_add_form)
        return render(request, self.template_name, context)
    
    def add_cafe_product(self, request):
        cafe_product_form = CafeProductForm(request.POST, request.FILES)
        if cafe_product_form.is_valid():
            cafe_product_form.save()
            return redirect('/admin-main-page/')
        
        context = self.get_context_data(cafe_product_form=cafe_product_form)
        return render(request, self.template_name, context)

    def update_cafe_product(self, request, cafe_product_id):
        cafe_product = get_object_or_404(CafeProduct, id=cafe_product_id)
        cafe_product_form = CafeProductForm(request.POST, request.FILES, instance=cafe_product)
        if cafe_product_form.is_valid():
            cafe_product_form.save()
            return redirect('/admin-main-page/')

        context = self.get_context_data(cafe_product_form=cafe_product_form)
        return render(request, self.template_name, context)
    
    def add_type_cafe_product(self, request):
        type_cafe_product_form = AddTypeCafeProductForm(request.POST)
        if type_cafe_product_form.is_valid():
            type_cafe_product_form.save()
            return redirect('/admin-main-page/')

        context = self.get_context_data(add_type_cafe_product_form=type_cafe_product_form)
        return render(request, self.template_name, context)

    def update_type_cafe_product(self, request, type_cafe_product_id):
        type_cafe_product = get_object_or_404(TypeCafeProduct, id=type_cafe_product_id)
        type_cafe_product_form = UpdateTypeCafeProductForm(request.POST, instance=type_cafe_product)
        if type_cafe_product_form.is_valid():
            type_cafe_product_form.save()
            return redirect('/admin-main-page/')

        context = self.get_context_data(type_cafe_product_form=type_cafe_product_form)
        return render(request, self.template_name, context)
    
    def add_gallery(self, request):
        add_gallery_form = AddGalleryForm(request.POST, request.FILES)
        if add_gallery_form.is_valid():
            add_gallery_form.save()
            return redirect('/admin-main-page/')
        
        context = self.get_context_data(add_gallery_form=add_gallery_form)
        return render(request, self.template_name, context)

    def render_to_response(self, context, **response_kwargs):
        context.update(self.get_context_data())
        return render(self.request, self.template_name, context, **response_kwargs)
    

class RecordView(View):
    template_name = 'record.html'

    def get(self, request):
        step = request.GET.get('step', '1')
        context = self.get_context_data(step, request)
        return render(request, self.template_name, context)

    def post(self, request):
        step = request.POST.get('step', '1')
        if step == '1':
            return self.choice_of_procedure(request)
        elif step == '2':
            return self.choice_of_therapist(request)
        elif step == '3':
            return self.choice_of_datetime(request)
        context = self.get_context_data(step, request)
        return render(request, self.template_name, context)

    def get_context_data(self, step, request):
        context = {
            'step': step,
            'procedure_form': ProcedureForm(),
            'therapist_form': TherapistForm(),
            'schedule_form': ScheduleForm(),
        }
        if step == '1':
            context['spa_categories'] = SpaСategories.objects.all()
            context['procedures'] = Procedure.objects.all()
        if step == '2':
            context['therapists'] = self.sorting_therapists(request)
        if step == '3':
            context.update(self.get_available_slots(request))
        return context

    def get_available_slots(self, request):
        procedure = Procedure.objects.get(id=request.session['procedure_id'])
        therapist = MassageTherapist.objects.get(id=request.session['therapist_id'])
        schedules = Schedule.objects.filter(therapist=therapist, day__gte=datetime.now().date())
        available_slots = {}
        now = datetime.now()

        for schedule in schedules:
            validator = SlotsValidator(schedule, procedure)
            date_str = schedule.day.strftime('%Y-%m-%d')
            available_slots[date_str] = [
                slot for slot in validator.ranges
                if datetime.combine(schedule.day, datetime.strptime(slot, '%H:%M').time()) > now
            ]

        taken_slots = Record.objects.filter(
            schedule__therapist=therapist,
            schedule__day__gte=datetime.now().date()
        ).values_list('schedule__day', 'start_time')
        occupied_slots = {(date.strftime('%Y-%m-%d'), time.strftime('%H:%M')) for date, time in taken_slots}
        # Удаляем занятые слоты из available_slots
        for date_str, slots in available_slots.items():
            available_slots[date_str] = [time for time in slots if (date_str, time) not in occupied_slots]

        # Убираем даты без доступных слотов
        available_slots = {date: slots for date, slots in available_slots.items() if slots}

        return {'available_slots': available_slots}
    
    def choice_of_procedure(self, request):
        procedure_id = request.POST.get('procedure')
        if procedure_id:
            request.session['procedure_id'] = procedure_id
            return redirect('/create-record/?step=2')
        return redirect('/create-record/')
    
    def choice_of_therapist(self, request):
        therapist_form = TherapistForm(request.POST)
        if therapist_form.is_valid():
            request.session['therapist_id'] = therapist_form.cleaned_data['therapist'].id
            return redirect('/create-record/?step=3')
        return redirect('/create-record/?step=2')
    
    def choice_of_datetime(self, request):
        date = request.POST.get('date')
        time = request.POST.get('time')
        if date and time:
            procedure = Procedure.objects.get(id=request.session['procedure_id'])
            therapist = MassageTherapist.objects.get(id=request.session['therapist_id'])
            user = request.user
            date = datetime.strptime(date, '%Y-%m-%d').date()
            time = datetime.strptime(time, '%H:%M').time()
            start_time = datetime.combine(date, time)
            end_time = start_time + procedure.duration

            # Проверка на существующие записи
            overlapping_records = Record.objects.filter(
                schedule__therapist=therapist,
                schedule__day=date
            ).exclude(
                start_time__gte=end_time.time()
            ).exclude(
                start_time__lt=start_time.time()
            )

            if overlapping_records.exists():
                context = self.get_context_data('3', request)
                context['error_message'] = "На это время уже есть запись. Пожалуйста, выберите другое время."
                return render(request, self.template_name, context)

            # Создание новой записи
            schedule, created = Schedule.objects.get_or_create(
                therapist=therapist,
                day=date,
                defaults={'start_time': time, 'end_time': end_time.time()}
            )
            Record.objects.create(schedule=schedule, procedure=procedure, start_time=time, client=user)
            return redirect('/create-record/')

        context = self.get_context_data('3', request)
        return render(request, self.template_name, context)

    def sorting_therapists(self, request):
        procedure = Procedure.objects.get(id=request.session['procedure_id'])
        now = datetime.now()
        therapists = MassageTherapist.objects.filter(
        position__spa_categories=procedure.type_category.categories,
        schedule__day__gte=now.date()
    ).distinct().order_by('-average_rating')

        therapists_with_slots = []

        for therapist in therapists:
            schedules = Schedule.objects.filter(therapist=therapist, day__gte=now.date()).order_by('day')
            nearest_slots = []

            for schedule in schedules:
                if nearest_slots:
                    break
                validator = SlotsValidator(schedule, procedure)
                slots = [
                    slot for slot in validator.ranges
                    if datetime.combine(schedule.day, datetime.strptime(slot, '%H:%M').time()) > now
                ]
                nearest_slots.extend({'date': schedule.day.strftime('%Y-%m-%d'), 'time': slot} for slot in slots[:5])

            if nearest_slots:
                therapists_with_slots.append({
                    'therapist': therapist,
                    'nearest_slots': nearest_slots[:5]
                })

        return therapists_with_slots