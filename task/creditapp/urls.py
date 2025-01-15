from django.urls import path
from . import views

urlpatterns = [
    path('register-user/', views.UserRegistrationView.as_view({'post': 'create'})),
    path('apply-loan/', views.LoanApplicationView.as_view({'post': 'create'})),
    path('make-payment/', views.make_payment),
    path('get-statement/', views.get_statement),
]