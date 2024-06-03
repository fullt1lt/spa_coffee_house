from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login
from forms.forms import LoginUserForm, MassageTherapistForm, RegisterUserForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DeleteView, UpdateView,CreateView

from myspa.models import MassageTherapist, SpaUser
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
    
     
class HomePage(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


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