from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, UpdateView, CreateView
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        active_version = product.versions.filter(is_current_version=True).first()
        context['active_version'] = active_version
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем продукт к текущему пользователю
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:home')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:home')

    def test_func(self):
        return self.get_object().user == self.request.user  # Проверяем, что пользователь является владельцем продукта

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'

    def get_success_url(self):
        return reverse('catalog:home')

    def test_func(self):
        return self.get_object().user == self.request.user  # Проверяем, что пользователь является владельцем продукта


class VersionCreateView(View):
    template_name = 'catalog/version_form.html'

    def get(self, request):
        form = VersionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VersionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Замените 'success_url' на ваш реальный URL
        return render(request, self.template_name, {'form': form})
