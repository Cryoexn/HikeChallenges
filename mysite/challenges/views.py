from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from users.models import Achievement
from datetime import datetime

from .models import Challenge, Mountain
from .forms import AchievementForm
from .weatherutils import get_weather

def index_view(request):
    try:
        # Get the list of challenges listed by name.
        challenge_list = Challenge.objects.order_by('challenge_name')
    except ObjectDoesNotExist:
        raise Http404('There are currently no challenges.')

    return render(request, 'challenges/index.html', {'challenge_list' : challenge_list,})

def challenge_detail_view(request, challenge_name):
    try:
        # If the challenge exists in the database display the details page.
        challenge = Challenge.objects.get(challenge_name=challenge_name)

        mountain_list = challenge.mountains.all()

    except ObjectDoesNotExist:
        raise Http404(challenge_name + " Challenge does not exist.")

    ach_list = None
    
    # Check if the user is authenticated.
    # if the user is authenticated give details about the challenge.
    # if the user is not authenticated send no details.
    if request.user.is_authenticated:
        ach_list = Achievement.objects.filter(user=request.user)
    
    mnt_progress = 0
    elv_progress = 0
    dis_progress = 0

    total_elv = 0
    total_dis = 0

    if ach_list:
        for ach in ach_list:
            if ach.mountain_completed:
                for mountain in mountain_list:
                    total_elv += mountain.elevation
                    total_dis += mountain.distance
                    if ach.mountain_completed.mnt_name == mountain.mnt_name:
                        mnt_progress += 1
                        elv_progress += mountain.elevation
                        dis_progress += mountain.distance 

        if len(mountain_list) > 0:
            mnt_progress = round((mnt_progress / len(mountain_list)) * 100)

        if total_elv > 0:    
            elv_progress = round((elv_progress / total_elv) * 100)

        if total_dis > 0:
            dis_progress = round((dis_progress / total_dis) * 100)

    if not request.user.is_authenticated:
        messages.warning(request, 'You need to be logged in to view mountain details. You will be redirected to login page.')

    context = {
        'mountain_progress' : mnt_progress,
        'elevation_progress' : elv_progress,
        'distance_progress' : dis_progress,
        'challenge_name' : challenge_name,
        'mountains_list' : mountain_list,
    }

    return render(request, 'challenges/challenge_detail.html', context)

@login_required
def mountain_detail_view(request, challenge_name, mnt_name):
    try:
        mountain = Mountain.objects.get(mnt_name=mnt_name)
    except ObjectDoesNotExist:
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

    if len(weather) > 1:
        context = {
            'mountain'   : mountain,
            'challenge_name': challenge_name,
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
            'challenge_name' : challenge_name,
            'completed'  : None,
            'curr_days'  : None,
            'week_days'  : None,
            'week_nights': None,
            'rel_city'   : "N/A",
            'error_msg'  : f"Weather could not be fetched. { weather }. Try refreshing the page.",
        }

    return render(request, 'challenges/mountain_detail.html', context)

def achievement_edit_view(request, challenge_name, mnt_name):
    if request.user.is_authenticated:
        user_achievements = Achievement.objects.filter(user=request.user)
    
    ach = Achievement(user=request.user)

    if user_achievements:
        for achievement in user_achievements:
            if achievement.mountain_completed:
                if achievement.mountain_completed.mnt_name == mnt_name:
                    ach = achievement

    ach_form = AchievementForm()

    context = {
        'mnt_name'   : mnt_name,
        'ach_form'   : ach_form,
        'chall_name' : challenge_name,
        'achievement': ach,
    }

    return render(request, 'challenges/achievement_edit.html', context)