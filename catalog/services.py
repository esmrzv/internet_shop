from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


# def get_products_from_cache():
#     if not CACHED_ENABLED:
#         return Product.objects.all()
#     key = 'product_list'
#     product = cache.get(key)
#     if product is not None:
#         return product
#     product = Product.objects.all()
#     cache.set(key, product)
#     return product


def get_category_from_cache():
    """
    Возвращает список продуктов из кэша или из базы,
    если кэш не включен.
    """
    if not CACHE_ENABLED:  # если кэш не включен
        return Product.objects.all()  # возвращаем список продуктов
    key = 'category_list'  # ключ
    product = cache.get(key)  # получаем кэш по ключу
    if product is not None:  # если кэш не пустой
        return product  # возвращаем кэш
    product = Product.objects.all()  # получаем список продуктов из базы
    cache.set(key, product)  # кладем список продуктов в кэш
    return product
