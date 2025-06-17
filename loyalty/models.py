from django.db import models
from accounts.models import Account

class LoyaltyPoint(models.Model):
    user       = models.OneToOneField(Account, on_delete=models.CASCADE) 
    points     = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} — {self.points} pts"
    

    def add_points(self, amount):
        self.points += amount
        self.save()

    def redeem_points(self, amount):
        if self.points  >= amount:
            self.points -= amount
            self.save()


class Reward(models.Model):
    REWARD_TYPES = [
        ('cinema', 'Cinema Ticket'),
        ('discount', 'Percentage Discount'),
    ]
    title                = models.CharField(max_length=100)
    description          = models.TextField(blank=True)
    owner                = models.CharField(max_length=100, default="senuoy")
    image                = models.ImageField(upload_to='loyality/')
    points_required      = models.IntegerField()
    reward_type          = models.CharField(max_length=20, choices=REWARD_TYPES)
    discount_percent     = models.IntegerField(null=True, blank=True)
    cinema_ticket_code   = models.CharField(max_length=100, blank=True, null=True, unique=True)
    conditions_generales = models.CharField(max_length=255, blank=True, null=True)
 
    def __str__(self):
        return self.title



class RedeemedReward(models.Model):
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    reward      = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    used        = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.title}"

