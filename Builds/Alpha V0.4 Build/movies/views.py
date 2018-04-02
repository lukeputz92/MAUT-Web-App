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
			print(criteria_list)
			print([i[1] for i in criteria_list])
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
			return HttpResponseRedirect('/movies/scores/')
	else:
		movieAutoScoreForm = MovieAutoScoreForm(criteria_list = [i[0] for i in request.session['criteria_list']])
	return render(request, 'movies/movie_auto_scores.html', {"movieAutoScoreForm" : movieAutoScoreForm})