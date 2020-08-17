from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .weatherutils import get_weather
from .models import Challenge, Mountain
from users.models import Achievement
from datetime import datetime

def index_view(request):
    try:
        # Get the list of challenges listed by name.
        challenge_list = Challenge.objects.order_by('challenge_name')
    except Challenge.DoesNotExist:
        raise Http404('There are currently no challenges.')

    return render(request, 'challenges/index.html', {'challenge_list' : challenge_list,})

def challenge_detail_view(request, challenge_name):
    try:
        # If the challenge exists in the database display the details page.
        challenge = Challenge.objects.get(challenge_name=challenge_name)

        mountains_list = challenge.mountains.all()

    except Challenge.DoesNotExist:
        raise Http404(challenge_name + " Challenge does not exist.")

    return render(request, 'challenges/challenge_detail.html', {'challenge_name' : challenge_name, 'mountains_list' : mountains_list,})

@login_required
def mountain_detail_view(request, challenge_name, mnt_name):
    try:
        mountain = Mountain.objects.get(mnt_name=mnt_name)
    except Mountain.DoesNotExist:
        raise Http404(mnt_name + " does not exist.")
    
    if request.user.is_authenticated:
        user_achievements = Achievement.objects.filter(user=request.user)
    
    completed = False
    date_completed = "N/A"

    for achievement in user_achievements:
        if achievement.mountain_completed:
            if achievement.mountain_completed.mnt_name == mnt_name:
                completed = True
                date_completed = achievement.date_completed.strftime("%b %d, %Y")

    # icons link might be broken for api queries.
    weather = get_weather(mountain.longitude, mountain.latitude)

    if weather:
        context = {
            'mountain'   : mountain,
            'completed'  : completed,
            'date_completed'  : date_completed,
            'curr_days'  : weather[0],
            'week_days'  : weather[1],
            'week_nights': weather[2],
            'rel_city'   : weather[3],
        }
    else:
        context = {
            'mountain'   : mountain,
            'completed'  : None,
            'curr_days'  : None,
            'week_days'  : None,
            'week_nights': None,
            'rel_city'   : "N/A",
            'error_msg'  : "Weather could not be fetched. Try refreshing the page.",
        }

    return render(request, 'challenges/mountain_detail.html', context)