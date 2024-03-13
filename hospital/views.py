from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import actionHistory
from .env_world import Game
from .forms import performActionForm

# Create your views here.
def index(request):
    return render(request, 'hospital/index.html')

@csrf_exempt
def performAction(request):
    pastActions = []
    cmds = []
    history = actionHistory.objects.all()
    for action in history:
        pastActions.append({
            'action': action.action,
            'observation': action.observation
        })
        cmds.append(action.action)

    game = Game()
    nextAct = game.start(cmds)

    if request.method == 'POST':
        form = performActionForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            
            cmds.append(res.action)
            game = Game()
            nextAct = game.start(cmds)
            actionHistory.objects.create(action=res.action, observation=nextAct['observation'])

            return redirect('performAction')
        else:
            return HttpResponse(form.errors.as_json())
    else:
        form = performActionForm()
    return render(request, 'hospital/performAction.html', {
        'form': form,
        'title': 'Actions',
        'pastActions': pastActions,
        'nextAction': nextAct,
    })

def reset(request):
    actionHistory.objects.all().delete()
    action_initial = "initialise"
    obc_initial = "You are in the hallway. This room is called the hallway. This is the main corridor in the ground floor from which we can go to other rooms. The rooms that we can go from here are : doctor chamber #1, doctor chamber #2, general ward, icu ward, common toilet, Nurse Station. The room contains : wall poster, doctor #1, agent."
    actionHistory.objects.create(action=action_initial, observation=obc_initial)
    return redirect('performAction')