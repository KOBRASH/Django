from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, UpdateView, CreateView
from catalog.forms import ProductForm, VersionForm, ProductDescriptionForm, ProductCategoryForm
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

    def test_func(self):
        # Проверяем, имеет ли пользователь право изменять продукт
        product = self.get_object()
        return product.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return HttpResponseForbidden()  # Возвращаем ошибку 403 Forbidden
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'

    def get_success_url(self):
        return reverse('catalog:home')

    def test_func(self):
        return self.get_object().user == self.request.user  # Проверяем, что пользователь является владельцем продукта


class CancelProductPublicationView(UserPassesTestMixin, DetailView):
    model = Product
    template_name = 'catalog/cancel_product_publication.html'

    def test_func(self):
        # Проверяем, имеет ли пользователь право отменять публикацию продуктов
        return self.request.user.has_perm('catalog.set_published')

    def post(self, request, *args, **kwargs):
        # Получаем объект продукта по его идентификатору
        product = self.get_object()

        # Отменяем публикацию продукта
        product.is_published = False
        product.save()

        # Перенаправляем пользователя на указанный URL
        return redirect('catalog:home')  # Замените на URL вашего приложения, куда нужно перенаправить после отмены публикации

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


class ChangeProductDescriptionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Проверяем, имеет ли пользователь право изменять описание продуктов
        return self.request.user.has_perm('catalog.change_description')

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductDescriptionForm(instance=product)
        return render(request, 'catalog/change_product_description.html', {'form': form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductDescriptionForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_detail', pk=pk)
        return render(request, 'catalog/change_product_description.html', {'form': form})


class ChangeProductCategoryView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Проверяем, имеет ли пользователь право изменять категорию продуктов
        return self.request.user.has_perm('catalog.change_category')

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductCategoryForm(instance=product)
        return render(request, 'catalog/change_product_category.html', {'form': form, 'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductCategoryForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_detail', pk=pk)
        return render(request, 'catalog/change_product_category.html', {'form': form, 'product': product})


