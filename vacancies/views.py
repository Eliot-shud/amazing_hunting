import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from vacancies.models import Vacancy, Skill
from vacancies.permissions import VacancyCreatePermission
from vacancies.serializers import VacancySerializer, VacancyListSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDeleteSerializer, SkillSerializer


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )
        skills = request.GET.getlist('text', None)
        skills_q = None
        for skill in skills:
            if skills_q is None:
                skills_q = Q(skills__name__icontains=skill)
            else:
                skills_q |= Q(skills__name__icontains=skill)

        if skills_q:
            self.queryset = self.queryset.filter(skills_q)

        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated]


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDeleteSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_vacancies(self, request):
        users_qs = User.objects.annotate(vacancies=Count('vacancy'))

        paginator = Paginator(users_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []
        for user in users_qs:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacancies": user.vacancies,
            })

        response = {
            "items": users,
            "avg": users_qs.aggregate(Avg('vacancies')),
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }
        return JsonResponse(response, safe=False)


class VacancyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailView

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(
            VacancyDeleteSerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data,
            safe=False
        )
