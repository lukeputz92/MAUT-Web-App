from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
#from .models import UserProfile, Decide, Item, Criteria
from django.shortcuts import render, redirect, render_to_response
from .movies_api import *
from decisions.models import *
import json

def movie_criteria(request):
	if request.method == 'POST':
		movieCriteriaForm = MovieCriteriaForm(request.POST)
		if movieCriteriaForm.is_valid():
			criteria_options = []
			for i in range(len(APIT)):
				if movieCriteriaForm.cleaned_data[str(i)]:
					criteria_options.append(APIT[i])
			request.session['criteria_list'] = criteria_options
			return HttpResponseRedirect('/movies/criteria_weight/')

	else:
		movieCriteriaForm = MovieCriteriaForm()

	return render(request, 'movies/movie_criteria.html',{'movieCriteriaForm' : movieCriteriaForm})

def movie_criteria_weight(request):
	if request.method == 'POST':
		movieCriteriaWeightForm = MovieCriteriaWeightForm(request.POST, criteria_list = [i['name'] for i in request.session['criteria_list']])
		if movieCriteriaWeightForm.is_valid():
			criteria_list = request.session['criteria_list']
			for i in range(len(criteria_list)):
				criteria_list[i] = (criteria_list[i],movieCriteriaWeightForm.cleaned_data[str(i)],0)
			request.session['criteria_list'] = criteria_list
			return HttpResponseRedirect('/movies/auto_scores/')

	else:
		movieCriteriaWeightForm = MovieCriteriaWeightForm(criteria_list = [i['name'] for i in request.session['criteria_list']])
	criteriaList = [i['name'].replace(' ','+') for i in request.session['criteria_list']]
	criteriaList = json.dumps(criteriaList).replace(' ','')
	return render(request, 'movies/movie_criteria_weight.html', {"criteriaList" : criteriaList, "weightForm" : movieCriteriaWeightForm})

def movie_auto_scores(request):
	if request.method=='POST':
		movieAutoScoreForm = MovieAutoScoreForm(request.POST, criteria_list = [i[0] for i in request.session['criteria_list']])
		if movieAutoScoreForm.is_valid():
			criteria_list = request.session['criteria_list']
			for i in range(len(criteria_list)):
				criteria_list[i] = (criteria_list[i][0], criteria_list[i][1], movieAutoScoreForm.cleaned_data[str(i)])
				request.session['criteria_list'] = criteria_list
			print(request.session['criteria_list'])
			return HttpResponseRedirect('/movies/scores/')
	else:
		movieAutoScoreForm = MovieAutoScoreForm(criteria_list = [i[0] for i in request.session['criteria_list']])
	return render(request, 'movies/movie_auto_scores.html', {"movieAutoScoreForm" : movieAutoScoreForm})

def auto_scorer(num,max,min,asc):
	if max==min:
		return 100
	if asc:
		return((100*(max-num))/(max-min))
	else:
		return ((100*(num-min))/(max-min))


def movie_scores(request):
	movs = MOVIES
	for m in movs:
		x = auto_scorer(float(m['Year of Release']),maxYear,minYear, request.session['criteria_list'][0][2]) * request.session['criteria_list'][0][1] / 100
		y = auto_scorer(float(m['Year of Release']),maxYear,minYear, request.session['criteria_list'][1][2]) * request.session['criteria_list'][1][1] / 100
		m['finalScore'] = round(x+y,2)
	movieList = movs
	request.session['movieList'] = movieList
	print(movieList)
	return render(request, 'movies/movie_results.html', {"request" : request, "movieList" : movieList, "length" : len(movieList)})
'''
def movie_results(request):
	if request.method == 'POST':
		user = User.objects.get(username=request.user.username)
		profile = UserProfile.objects.get(user=user)
		newDecision = Decide(user_profile = profile, decisionName = "Movie")
		newDecision.save()
		movieList = request.session['movieList']
		criteriaList = request.session['criteria_list']
		for movie in movieList:
			newItem = Item(itemName = movie[0], itemScore = movie[-1], decision = newDecision)
			newItem.save()
		for criteria in criteriaList:
			newCriteria = Criteria(criteriaName = criteria[0]['name'], criteriaWeight = criteria[1], decision = newDecision)
			newCriteria.save()
		request.session['saved'] = True
	else:
		request.session['saved'] = False
		movieList = request.session['movieList']
		movieList = sorted(movieList, key = lambda x: x['finalScore'],reverse=True)
		print(movieList)
		request.session['movieList'] = movieList
	return render(request, 'movies/movie_results.html', {"request" : request, "movieList" : movieList, "length" : len(movieList)})


'''


