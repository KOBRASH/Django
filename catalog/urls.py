from catalog.apps import CatalogConfig
from django.views.decorators.cache import cache_page
from django.urls import path
from catalog.views import HomeView, ContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, VersionCreateView, CancelProductPublicationView, ChangeProductDescriptionView, \
    ChangeProductCategoryView

app_name = CatalogConfig.name




urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/cancel-publication/', CancelProductPublicationView.as_view(), name='cancel_product_publication'),
    path('product/<int:pk>/change-description/', ChangeProductDescriptionView.as_view(), name='change_product_description'),
    path('product/<int:pk>/change-category/', ChangeProductCategoryView.as_view(), name='change_product_category'),
    path('version/create/', VersionCreateView.as_view(), name='version_create')
]
