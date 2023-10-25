from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import Account, Election, Ballot, Vote, Candidate



# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username, password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        user = User(username = username, password=password)
        user.save()
        account_ins = Account.objects.create(user=user, account_type = user_type, first_name = first_name, last_name = last_name, date_of_birth = date_of_birth)
        account_ins.save()
        return redirect('home')
    return render(request, 'register.html')

def user_logout(request):
    return logout(request)

def create_election(request):
    curr_user = request.user
    curr_acc = Account.objects.get(user=curr_user)
    if curr_acc.account_type == 'admin':
        if request.method == 'POST':
            name = request.POST['name']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']

            if name and start_date and end_date:
                Election.objects.create(name=name, start_date=start_date, end_date=end_date)
                return redirect('/')
            else:
                return HttpResponse("Error parsing data, Please try again.")
        return render(request, 'create_election.html')
    return HttpResponse("The account is not admin type. Please login from admin account.")

def add_candidate(request, election_id):
    context = {}
    election = Election.objects.get(pk=election_id)

    if request.method == 'POST':
        curr_user = request.user
        curr_account = Account.objects.get(user=curr_user)
        if curr_account.account_type == 'admin':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            date_of_birth = request.POST['date_of_birth']
            group_name = request.POST['group_name']

            if first_name and last_name and date_of_birth and group_name:
                candidate_ins = Candidate(first_name=first_name, last_name = last_name, date_of_birth=date_of_birth, group_name=group_name, election = election)
                candidate_ins.save()
                return redirect('/')
            else:
                return HttpResponse("Fill the form properly")
        else:
            return HttpResponse("You are not allowed to fill the form")
    context['election'] = election
    return render(request, 'candidate_register.html', context)


def create_ballot(request, election_id):
    election = Election.objects.get(pk=election_id)
    context = {}
    if request.method == 'POST':
        title = request.POST['title']
        if title:
            Ballot.objects.create(election=election, title=title)

            return redirect('/')
    context['election'] = election
    return render(request, 'create_ballot.html', context)


def issue_vote(request, ballot_id):
    context = {}
    ballot = Ballot.objects.get(pk = ballot_id)
    election = ballot.election

    if request.metod == 'POST':
        candidate_id = request.POST['candidate']
        user = request.user

        if not Vote.objects.filter(user=user, ballot=ballot).exists():
            candidate = Candidate.objects.get(pk = candidate_id)
            Vote.objects.create(user = user, ballot = ballot, candidate = candidate)
            return redirect('/')
    candidates = Candidate.objects.filter(election = election)
    context['ballot'] = ballot
    context['candidates'] = candidates
    return render(request, 'issue_vote.html', context)

def election_result(request, election_id):
    election = Election.objects.get(pk=election_id)
    candidates = Candidate.objects.filter(election = election)
    context = {}
    results = {}
    for candidate in candidates:
        vote_counts = Vote.objects.filter(candidate=candidate).count()
        results[candidate] = vote_counts
    sorted_result = sorted(results.items(), key=lambda x : x[1], reverse=True)
    context['election'] = election
    context['results'] = sorted_result
    return render(request, 'election_results.html', context)