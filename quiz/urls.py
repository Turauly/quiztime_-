from django.urls import path
from .views import (
    quiz_view,
    statistics_view,
    suggest_question_view,
    schedule_view,
    edit_schedule,
    delete_schedule,
    course_list  # ✅ осыны қостық
)

urlpatterns = [
    path('', quiz_view, name='quiz'),
    path('statistics/', statistics_view, name='statistics'),
    path('suggest/', suggest_question_view, name='suggest_question'),
    path('schedule/', schedule_view, name='schedule'),
    path('schedule/edit/<int:pk>/', edit_schedule, name='edit_schedule'),
    path('schedule/delete/<int:pk>/', delete_schedule, name='delete_schedule'),
    path('courses/', course_list, name='course_list'),
]
