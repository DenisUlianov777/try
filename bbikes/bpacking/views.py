from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import *

from .forms import *
from .models import *
from .permissions import *
from .serializers import BikesSerializer


class Home(ListView):
    paginate_by = 5
    template_name = 'bpacking/index.html'
    context_object_name = 'posts'  # вместо object_list в шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Bike.objects.filter(is_published=Bike.Status.PUBLISHED).select_related('cat')


@login_required  # доступ для авторизованных
def about(request):
    contact_list = Bike.objects.all()
    paginator = Paginator(contact_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bpacking/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'bpacking/addpage.html'
    login_url = reverse_lazy('login')
    extra_context = {
        'title': 'Добавление статьи',
    }

    def form_valid(self, form):
        w = form.save(commit=False)
        w.auth_user = self.request.user
        return super().form_valid(form)


class UpdatePage(UserPassesTestMixin, UpdateView):
    model = Bike
    fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
    template_name = 'bpacking/updatepage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Редактирование статьи',
    }

    def test_func(self):
        obj = self.get_object()
        return obj.auth_user == self.request.user

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'bpacking/contact.html'
    extra_context = {'title': "Обратная связь"}
    success_url = reverse_lazy('home')


class ShowPost(DetailView):
    model = Bike
    template_name = 'bpacking/post.html'
    # slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Bike.published, slug=self.kwargs['slug'])


class BikeCategory(ListView):
    template_name = 'bpacking/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['cat_selected'] = cat.id
        return context

    def get_queryset(self):
        return Bike.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'bpacking/login.html'
    extra_context = {'title': 'Авторизация'}


    # def get_success_url(self):
    #     return reverse_lazy('home')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'bpacking/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('login')


class BikesViewSet(viewsets.ModelViewSet):
    queryset = Bike.objects.all()
    serializer_class = BikesSerializer
    permission_classes = (IsAdminOrReadOnly)

    # def get_queryset(self):
    #     pk = self.kwargs.get("pk")
    #
    #     if not pk:
    #         return Bike.objects.all()[:2]
    #
    #     return Bike.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        cats = Category.objects.get(pk=pk)
        return Response({'cats': cats.name})


class BikeTags(ListView):
    template_name = 'bpacking/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Tags.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + c.tag
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Bike.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class Profile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'bpacking/profile.html'
    extra_context = {'title': "Профиль пользователя", 'default_img': settings.DEFAULT_USER_IMAGE}


    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "bpacking/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}

