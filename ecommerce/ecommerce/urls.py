from django.urls import path
from authentication.views import SignupView, LoginView
from products.views import ProductListCreateView
from orders.views import OrderListCreateView, OrderAssignView, OrderStatusUpdateView, OrderReportView

urlpatterns = [
    path('api/auth/signup/', SignupView.as_view()),
    path('api/auth/login/', LoginView.as_view()),
    path('api/products/', ProductListCreateView.as_view()),
    path('api/orders/', OrderListCreateView.as_view()),
    path('api/orders/<int:order_id>/assign/', OrderAssignView.as_view()),
    path('api/orders/<int:order_id>/status/', OrderStatusUpdateView.as_view()),
    path('api/reports/orders/', OrderReportView.as_view()),
]