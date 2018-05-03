from django.conf.urls import url
from .views import *
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^ticket/(?P<slug>[\w-]+)/$', views.get_ticket_by_slug, name='get_ticket_by_slug'),
    url(r'^(?P<slug>[\w-]+)/$', views.get_ticket_by_slug_to_user, name='get_ticket_by_slug_to_user'),
    url(r'^ticket/(?P<ticket>[\w-]+)/product/(?P<product>[\w-]+)$', views.add_product_to_ticket, name='add_product_to_ticket'),
    url(r'^ticket/(?P<ticket>[\w-]+)/product/(?P<product>[\w-]+)/delete/$', views.remove_product_from_ticket, name='remove_product_from_ticket'),
    url(r'^ticket/(?P<ticket>[\w-]+)/product/(?P<product>[\w-]+)/pay/$', views.pay_product_from_ticket, name='pay_product_from_ticket'),
    url(r'^ticket/(?P<slug>[\w-]+)/close/$', views.close_ticket_by_slug, name='close_ticket_by_slug'),
    url(r'^ticket/(?P<ticket>[\w-]+)/product/(?P<product>[\w-]+)/price/(?P<price>\d+\.\d{2})/$', views.add_product_without_price_to_ticket, name='add_product__without_price_to_ticket'),
    url(r'^ticket/(?P<ticket>[\w-]+)/discount/(?P<price>\d+\.\d{2})/$', views.give_discount_to_ticket, name='give_discount_to_ticket'),
    url(r'^invalid/ticket/$', views.show_invalid_page, name='show_invalid_page'),
    url(r'^api/products/(?P<name>.+)/$', ProductSearch.as_view()),
]

product_router = DefaultRouter()
product_router.register(r'products', ProductViewSet)
