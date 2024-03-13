from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import BlogPost
from django.utils.text import slugify

class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # Увеличение счетчика просмотров при открытии статьи
        obj = self.get_object()
        obj.views_count += 1
        obj.save()
        return super().get(request, *args, **kwargs)


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_create.html'
    fields = ['title', 'content', 'preview', 'published']

    def form_valid(self, form):
        instance = form.save(commit=False)
        slug = slugify(instance.title)

        # Проверка на уникальность slug
        count = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1

        instance.slug = slug
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'slug': self.object.slug})

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_update.html'
    fields = ['title', 'content', 'preview', 'published']

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'slug': self.object.slug})

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_delete.html'
    success_url = reverse_lazy('blog:list')

