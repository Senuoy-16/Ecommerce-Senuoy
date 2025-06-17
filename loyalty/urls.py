from django.urls import path
from . import views

app_name = 'loyalty'

urlpatterns = [
    path('home/', views.home_loyalty, name='home_loyalty'),
    path('rewards/list/', views.rewards_list, name='rewards_list'),
    path('reward_details/<int:reward_id>/', views.reward_details, name='reward_details'),
    path('get_reward/<int:reward_id>/', views.get_reward, name='get_reward'),
    path('rewards/gained/', views.rewards_gained, name='rewards_gained'), 
]