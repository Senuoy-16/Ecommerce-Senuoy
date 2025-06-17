from django.contrib import admin
from .models import LoyaltyPoint, Reward, RedeemedReward

@admin.register(LoyaltyPoint)
class LoyaltyPointAdmin(admin.ModelAdmin):
    list_display  = ['user','points', 'updated_at']
    list_filter   = ['user','points', 'updated_at']
    search_fields = ['user']


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display  = ['title','points_required', 'reward_type']
    list_filter   = ['reward_type']

@admin.register(RedeemedReward)
class RedeemedRewardAdmin(admin.ModelAdmin):
    list_display  = ['user','reward', 'redeemed_at', 'used']
    list_filter   = ['reward', 'used']