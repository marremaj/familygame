from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from .models import PlayerStatus,GameSession

import random

def startGame(request):
    if GameSession.objects.all().count() == 0:
        categories = ["Mat", "Verb", "Person", "Tal", "Djur", "Adjektiv", "Namn", "Transportmedel", "Känsla", "Yrke", "Plats", "Land", "Verktyg", "Sak"]
        category = categories[random.randint(0,len(categories) -1)]
        session = GameSession(code='Z1HJWW490000QQ', question="", state=0, category=category, voting_done=False)
        session.save()
    else:
        game = GameSession.objects.all()[0]
        categories = ["Mat", "Verb", "Person", "Tal", "Djur", "Adjektiv", "Namn", "Transportmedel", "Känsla", "Yrke", "Plats", "Land", "Verktyg", "Sak"]
        game.category = categories[random.randint(0,len(categories) -1)]
        game.question=""
        game.state=0
        game.master=None
        game.save()
        PlayerStatus.objects.delete()
    return HttpResponse("OK")

def getHomePage(request):
    return render(request, "homePage.html")

def chooseUsername(request):
    if (request.method == "POST"):
        name = request.POST['username']
        password = "DEFAULTPASSWORD"
        user = User.objects.create_user(name, password)
        player = PlayerStatus(user=user, points=0, answer="", done=False, session=GameSession.objects.all()[0])
        player.save()
        game = GameSession.objects.all()[0]
        print (game.master)
        if game.master == None:
            print("fake news")
            game.master = user
            game.save()
        login(request, user)
        return redirect("gamePage")
    else:
        if request.user.is_authenticated:
            game = GameSession.objects.all()[0]
            if game.master == None:
                game.master = request.user
                game.save()
            request.user.session=game
            request.user.save()
            return redirect("gamePage")
        return render(request, "addUserPage.html")

def getGamePage(request):
    game = GameSession.objects.all()[0]
    all_players = PlayerStatus.objects.filter(session=game)
    players = [player.user.username for player in all_players]
    if game.state == 0:
        if game.master == request.user:
            return render(request, "gamePage.html", {"master": True, "name":request.user, "players": players})
        return render(request, "gamePage.html", {"master": False, "name":request.user, "players": players})
    elif game.state >= 1:
        if game.master == request.user:
            return render(request, "addQuestion.html", {"master": True, "name":request.user, "category": game.category})
        return render(request, "addAnswers.html", {"master": False, "name":request.user, "category": game.category})
    else:
        return HttpResponse("Du e för sen eller så e marina fel")

def startRound(request):
    game = GameSession.objects.all()[0]
    game.state = 1
    game.save()
    return redirect("gamePage")

def getQuestion(request):
    game = GameSession.objects.all()[0]
    if (game.state == 2):
        return JsonResponse({"question": game.question, "done": True})
    else:
        return JsonResponse({"done": False})

def postAnswer(request):
    a = request.POST["answer"]
    p = PlayerStatus.objects.filter(user=request.user)[0]
    p.answer = a
    p.done = True
    p.save()
    return HttpResponse("OK")

def votingPage(request):
    return render(request, "votingPage.html")

def postQuestion(request):
    q = request.POST["question"]
    game = GameSession.objects.all()[0]
    game.question = q
    game.state = 2
    game.save()
    return render(request, "votingPage.html")

def votables(request):
    if (request.method == "POST"):
        v = request.POST["vote"]
        p = PlayerStatus.objects.filter(user_id=v)[0]
        p.votes = p.votes + 1
        p.save()
        game = GameSession.objects.all()[0]
        players = game.players.all()
        if sum([player.votes for player in players]) >= len(players):
            def mymax(x):
                return x["votes"]
            newlist = [{"userid": p.user.id, "name": p.user.username, "votes": p.votes, "score": p.points} for p in players]
            p = max(newlist, key=mymax)
            p.points = p.points + 1
            p.save()
            game.voting_done = True
            game.winner = p
        return HttpResponse("OK")
    else:
        game = GameSession.objects.all()[0]
        players = PlayerStatus.objects.filter(session=game)
        res = [{"user":player.user.id, "answer": player.answer} for player in players if player.done]
        print("---", res[0]["answer"])
        if len(res) == len(players) - 1:
            return JsonResponse({"done": True, "answers": res})
        return JsonResponse({"done": False})

def winningPage(request):
    return render(request, "winningPage.html")

def getWinner(request):
    game = GameSession.objects.all()[0]
    players = game.players.all()
    votingDone = game.voting_done
    def maxScore(x):
        return x["score"] +1
    def mymax(x):
        return x["votes"]
    if (votingDone):
        newlist = [{"userid": p.user.id, "name": p.user.username, "votes": p.votes, "score": p.points} for p in players]
        maxPlayer = max(newlist, key=mymax)
        game.master = User.objects.filter(id=maxPlayer["userid"])[0]
        game.state = 0
        game.save()
        return JsonResponse({"done": True, "winner": maxPlayer, "players": sorted(newlist, key=maxScore, reverse = True)})
    else:
        return JsonResponse({"done": False})

def resetRound(request):
    game = GameSession.objects.all()[0]
    categories = ["Mat", "Verb", "Person", "Tal", "Djur", "Adjektiv", "Namn", "Transportmedel", "Känsla", "Yrke", "Plats", "Land", "Verktyg", "Sak"]
    game.category = categories[random.randint(0,len(categories) - 1)]
    game.state = 0
    game.voting_done = False
    game.save()
    player = PlayerStatus.objects.filter(user=request.user)[0]
    player.votes = 0
    player.answer = ""
    player.done = False
    player.save()
    return redirect("gamePage")

def logout_view(request):
    #log out and delete user
    user = request.user
    logout(request)
    PlayerStatus.objects.filter(user=user).delete()
    user.delete()
    return redirect("home")