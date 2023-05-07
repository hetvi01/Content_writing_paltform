from django.urls import path

from writers.views import WriterRegistrationView, LoginView

urlpatterns = [
    path('register/', WriterRegistrationView.as_view(), name='writer-create'),
    path('login/', LoginView.as_view(), name='login'),
]