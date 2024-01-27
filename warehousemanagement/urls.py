from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add_product/', views.AddProductView.as_view(), name="add_product"),
    path('update_product/<int:product_id>/', views.UpdateProductView.as_view(), name="update_product"),
    path('inbound/', views.InboundView.as_view(), name="inbound"),
    path('outbound/', views.OutboundView.as_view(), name="outbound"),
]