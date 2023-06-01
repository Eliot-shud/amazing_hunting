from django.urls import path

from vacancies import views
from vacancies.views import VacancyListView, VacancyDetailView, VacancyCreateView, VacancyUpdateView, VacancyDeleteView

urlpatterns = [
    path('', VacancyListView.as_view()),
    path('create/', VacancyCreateView.as_view()),
    path('<int:pk>/', VacancyDetailView.as_view()),
    path('<int:pk>/update/', VacancyUpdateView.as_view()),
    path('<int:pk>/delete/', VacancyDeleteView.as_view()),
    path('<int:pk>/delete/', views.user_vacancies),
    path('like/', views.VacancyLikeView.as_view()),
]