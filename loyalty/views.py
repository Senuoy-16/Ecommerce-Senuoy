from django.shortcuts import render, get_object_or_404, redirect
from .models import LoyaltyPoint, Reward, RedeemedReward
from django.contrib.auth.decorators import login_required

import string, random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO

from .models import Reward, LoyaltyPoint, RedeemedReward
from coupons.models import Coupon 

@login_required
def home_loyalty(request):
    user    = request.user
    points  = get_object_or_404(LoyaltyPoint, user=user)
    context = {
        'user':user,
        'points':points,
    }
    return render(request, 'loyalty/home_loyalty.html', context)

@login_required
def rewards_list(request):
    rewards = Reward.objects.all()
    loyalty = LoyaltyPoint.objects.filter(user=request.user).first()
    points = loyalty.points if loyalty else 0
    context = {
        'rewards': rewards,
        'points': points,
    }
    return render(request, 'loyalty/rewards_list.html', context)

@login_required
def reward_details(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id)
    loyalty = LoyaltyPoint.objects.filter(user=request.user).first()
    points = loyalty.points if loyalty else 0
    context = {
        'reward': reward,
        'points': points,
    }
    return render(request, 'loyalty/reward_details.html', context)


def generate_coupon_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@login_required
def get_reward(request, reward_id):
    reward  = get_object_or_404(Reward, id=reward_id)
    loyalty, created = LoyaltyPoint.objects.get_or_create(user=request.user)

    if loyalty.points < reward.points_required:
        messages.error(request, "Vous n'avez pas assez de points.")
        return redirect('loyalty:rewards_list')


    # Deduct points
    loyalty.redeem_points(reward.points_required)

    # Save redemption
    RedeemedReward.objects.create(
        user=request.user,
        reward=reward,
        redeemed_at=timezone.now(),
        used=False
    )

    subject = "Votre récompense chez Senuoy"
    message = ""
    
    if reward.reward_type == "discount":
        # Create coupon valid for 1 year
        now = timezone.now()
        code = generate_coupon_code()
        coupon = Coupon.objects.create(
            code=code,
            valid_from=now,
            valid_to=now + timedelta(days=365),
            discount=reward.discount_percent ,
            active=True
        )

        message = (
            f"Félicitations ! Vous avez débloqué une réduction de {coupon.discount}%.\n\n"
            f"Code: {coupon.code}\n"
            f"Valable en ligne jusqu'au {coupon.valid_to.strftime('%d/%m/%Y')}.\n"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )

    elif reward.reward_type == "cinema":
        code = reward.cinema_ticket_code or "CODE-INDISPONIBLE"
        message = (
            f"Félicitations ! Vous avez débloqué un ticket de cinéma.\n\n"
        )
        context = {
            'code':code,
            'full_name':request.user.get_full_name,
        }
        html = render_to_string('loyalty/ticket_pdf.html', context)
        out = BytesIO()
        weasyprint.HTML(string=html).write_pdf(out)

        email = EmailMessage(
        subject=subject,
        body = message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.user.email]
        )
        email.attach(f'ticket_{code}.pdf', out.getvalue(), 'application/pdf')
        email.send()
        

    else:
        message = "Récompense débloquée, mais aucun type reconnu."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )

    context = {
        "message": "Récompense débloquée et envoyée par email !",
    }
    return render(request, 'loyalty/reward_done.html', context)



def rewards_gained(request):
    rewards = RedeemedReward.objects.filter(user=request.user)
    return render(request, 'loyalty/rewards_gained.html', {'rewards':rewards})






















