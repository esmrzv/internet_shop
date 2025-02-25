from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductManageForm
from catalog.models import Product, Version
from catalog.services import get_products_from_cache


class OwnerRequiredMixin(AccessMixin):
    """
    миксин для проверки владельца продукта.
    """

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет доступа к редактированию, удалению продуктов.")


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView, LoginRequiredMixin, OwnerRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Формирование формсета

        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (user.has_perm('catalog.can_change_is_published') and user.has_perm('catalog.can_change_description') and
                user.has_perm('catalog.can_change_category')):
            return ProductManageForm
        raise PermissionDenied


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for product in context['object_list']:
            versions = Version.objects.filter(product=product)
            active_versions = versions.filter(is_active=True)
            if active_versions:
                product.active_version = active_versions.last().version_name
            else:
                product.active_version = 'Нет активной версии'
        return context

    def get_queryset(self):
        return get_products_from_cache()


class ProductDetailView(DetailView, LoginRequiredMixin):
    model = Product


class ProductDeleteView(DeleteView, LoginRequiredMixin, OwnerRequiredMixin):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

