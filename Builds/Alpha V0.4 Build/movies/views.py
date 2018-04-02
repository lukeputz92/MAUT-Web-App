from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
#from .models import UserProfile, Decide, Item, Criteria
from django.shortcuts import render, redirect, render_to_response
from .movies_api import get_movies
from decisions.models import *

def MovieCriteria(request):
	if request.method = 'POST':
		movieCriteriaForm = MovieCriteriaForm(request.POST)
		if movieCriteriaForm.is_valid():
			criteria_options = []
			for i in range

	else:
		movieCriteriaForm = MovieCriteriaForm()

	return render(request, 'movies/movie_criteria.html',{'movieCriteriaForm' : movieCriteriaForm})
