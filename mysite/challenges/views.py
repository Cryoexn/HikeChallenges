from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
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

    # Set initial values.
    ach_list = None

    mnt_count = 0
    elv_count = 0
    dist_count = 0

    total_mnts = len(mountain_list)
    total_elv  = 0
    total_dist  = 0

    context = {
        'challenge_name' : challenge_name,
        'mountains_list' : mountain_list,
    }

    # Check if the user is authenticated.
    # if the user is authenticated give details about the challenge.
    # if the user is not authenticated send no details.
    if request.user.is_authenticated:
        ach_list = Achievement.objects.filter(user=request.user)
        completed_mountains = []
        
        if ach_list:
            for mountain in mountain_list:
                total_elv += mountain.elevation
                total_dist += mountain.distance
                for ach in ach_list:
                    if ach.mnt_completed:
                        if ach.mnt_completed.mnt_name == mountain.mnt_name:
                            completed_mountains.append(ach.mnt_completed)
                            mnt_count += 1
                            elv_count += mountain.elevation
                            dist_count += mountain.distance 

            if len(mountain_list) > 0:
                mnt_progress_pct = round((mnt_count / len(mountain_list)) * 100)
            else:
                mnt_progress_pct = 0

            if total_elv > 0:    
                elv_progress_pct = round((elv_count / total_elv) * 100)
            else:
                elv_progress_pct = 0

            if total_dist > 0:
                dist_progress_pct = round((dist_count / total_dist) * 100)
            else:
                dist_progress_pct = 0

            context = {
                'mountain_pct' : mnt_progress_pct,
                'mountain_frac': "{:,} / {:,}".format(mnt_count, total_mnts),
                'elevation_pct' : elv_progress_pct,
                'elevation_frac': "{:,} / {:,}".format(elv_count, total_elv),
                'distance_pct' : dist_progress_pct,
                'distance_frac' : "{:,} / {:,}".format(dist_count, total_dist),
                'challenge_name' : challenge_name,
                'mountains_list' : mountain_list,
                'completed_mountains': completed_mountains,
            }
    else:
        messages.warning(request, 'You need to be logged in to view mountain details. You will be redirected to login page.')



    return render(request, 'challenges/challenge_detail.html', context)

@login_required
def mountain_detail_view(request, challenge_name, mnt_name):
    try:
        mountain = Mountain.objects.get(mnt_name=mnt_name)
    except ObjectDoesNotExist:
        raise Http404(mnt_name + " does not exist.")
    
    if request.user.is_authenticated:
        user_achievements = Achievement.objects.filter(user=request.user)
    
    # Set default value for date completed.
    date_completed = "N/A"

    # For each achievement of user if the achievemnt has a mountain completed.
    # and the mountain completed is the current mountain.
    # get the date completed from the achievement.
    for achievement in user_achievements:
        if achievement.mnt_completed:
            if achievement.mnt_completed.mnt_name == mnt_name:
                date_completed = achievement.date_completed.strftime("%b %d, %Y")

    # get weather from database for the mountain longitude, latitude.
    weather = get_weather(mountain.longitude, mountain.latitude)

    # if the weather is a tuple (not error msg).
    if isinstance(weather, tuple):
        context = {
            'mountain'   : mountain,
            'challenge_name': challenge_name,
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
            'curr_days'  : None,
            'week_days'  : None,
            'week_nights': None,
            'rel_city'   : "N/A",
            'error_msg'  : f"Weather could not be fetched. { weather }. Try refreshing the page.",
        }

    return render(request, 'challenges/mountain_detail.html', context)

def achievement_edit_view(request, challenge_name, mnt_name):   

    if request.user.is_authenticated:
        ach = Achievement(user=request.user) 

        user_achievements = Achievement.objects.filter(user=request.user)

        if user_achievements:
            for achievement in user_achievements:
                if achievement.mnt_completed:
                    if achievement.mnt_completed.mnt_name == mnt_name:
                        ach = achievement

    if request.method == 'POST':
        # set the value for the form to the post request data.
        ach_form = AchievementForm(request.POST)

        if ach_form.is_valid():
            if ach_form.cleaned_data['date_done']:
                ach.date_completed = ach_form.cleaned_data['date_done']
                ach.mnt_completed = Mountain.objects.get(mnt_name=mnt_name)
            else:
                ach.mnt_completed = None
                ach.mnt_completed = None
                
            ach.save()

            return HttpResponseRedirect(f"/challenges/{challenge_name}/{mnt_name}")

    else :
        # set the value for the form to the achievement data.
        ach_form = AchievementForm({'date_done': ach.date_completed})

        context = {
            'mnt_name'   : mnt_name,
            'ach_form'   : ach_form,
            'chall_name' : challenge_name,
            'achievement': ach,
        }

    return render(request, 'challenges/achievement_edit.html', context)