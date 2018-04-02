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
		print(i)

	else:
		movieCriteriaWeightForm = MovieCriteriaWeightForm(criteria_list = [i['name'] for i in request.session['criteria_list']])
	criteriaList = [i['name'].replace(' ','+') for i in request.session['criteria_list']]
	criteriaList = json.dumps(criteriaList).replace(' ','')
	return render(request, 'movies/movie_criteria_weight.html', {"criteriaList" : criteriaList, "weightForm" : movieCriteriaWeightForm})