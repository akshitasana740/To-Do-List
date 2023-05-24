from django.shortcuts import render
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

# Create your views here.

class Login(LoginView):
    template_name='base/login.html'
    redirect_authenticated_user=True
    fields='__all__'
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name='base/register.html'
    success_url=reverse_lazy('tasks')
    form_class=UserCreationForm
    redirect_authenticated_user=True
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name='tasks'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.model.objects.filter(completed=False).count()-1
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='single_task'
    template_name='base/single_task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    success_url=reverse_lazy('tasks')
    fields = ['title', 'description', 'completed']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title', 'description', 'completed']
    success_url=reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    template_name='base/task_delete.html'
    success_url=reverse_lazy('tasks')