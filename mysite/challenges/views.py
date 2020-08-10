from django.shortcuts import render
from django.http import HttpResponse, Http404
from .weatherutils import get_weather
from .models import Challenge, Mountain


def home_view(request):
    return render(request, 'challenges/home.html')

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

        mountains_list = Mountain.objects.filter(challenge_id=challenge.id)

    except Challenge.DoesNotExist:
        raise Http404(challenge_name + " Challenge does not exist.")

    return render(request, 'challenges/challenge_detail.html', {'challenge_name' : challenge_name, 'mountains_list' : mountains_list,})

def mountain_detail_view(request, challenge_name, mnt_name):
    try:
        mountain = Mountain.objects.get(mnt_name=mnt_name)
    except Mountain.DoesNotExist:
        raise Http404(mnt_name + " does not exist.")
    
    # icons link might be broken for api queries.
    weather = get_weather(mountain.longitude, mountain.latitude)

    if weather:
        context = {
            'mountain'   : mountain,
            'curr_days'  : weather[0],
            'week_days'  : weather[1],
            'week_nights': weather[2],
            'rel_city'   : weather[3],
        }
    else:
        context = {
            'mountain'   : mountain,
            'rel_city'   : "N/A",
            'curr_days'  : None,
            'week_days'  : None,
            'week_nights': None,
            'error_msg'  : "Weather could not be fetched. Try refreshing the page.",
        }

    return render(request, 'challenges/mountain_detail.html', context)