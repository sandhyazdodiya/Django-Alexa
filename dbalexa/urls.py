from django.urls import path

from . import views
from . import my_skill
from .my_skill import skill,main

from django_ask_sdk.skill_adapter import SkillAdapter
my_skill_view = SkillAdapter.as_view(skill=skill)

urlpatterns = [
    path('index/', my_skill_view, name='index'),
    path('main/', my_skill.main, name='main'),

]


