from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name="home"),
    path('add_product/', views.AddProductView.as_view(), name="add_product"),
    path('update_product/<int:product_id>/', views.UpdateProductView.as_view(), name="update_product"),
    path('inbound/', views.InboundView.as_view(), name="inbound"),
    path('outbound/', views.OutboundView.as_view(), name="outbound"),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]