from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
#from .models import UserProfile, Decide, Item, Criteria
from django.shortcuts import render, redirect, render_to_response
from .cars_api import *
# Create your views here.

def cars(request):
    if request.method == 'POST':
        zipFilterForm = ZipFilterForm(request.POST)

        if zipFilterForm.is_valid():
            request.session['decision'] = CarsAPI()
            request.session['decision'].locationFilter(zipFilterForm.cleaned_data['zip_code'])

            return HttpResponseRedirect('/cars/criteria/')

    else:
        zipFilterForm = ZipFilterForm()

    return render(request, 'cars/index.html', {'zipFilterForm': zipFilterForm})

def cars_criteria(request):
    if request.method == 'POST':
        carsCriteriaForm = CarsCriteriaForm(request.POST)
        if carsCriteriaForm.is_valid():
            criteria_options = []
            for i in range(len(APIT)):
                if carsCriteriaForm.cleaned_data[str(i)]:
                    criteria_options.append(APIT[i])

            print(criteria_options)
            request.session['criteria_list'] = criteria_options

            return HttpResponseRedirect('/cars/criteria_weight/')
    else:
        carsCriteriaForm = CarsCriteriaForm()

    return render(request, 'cars/cars_criteria.html', {"carsCriteriaForm" : carsCriteriaForm})

def cars_criteria_weight(request):
    if request.method == 'POST':
        carsCriteriaWeightForm = CarsCriteriaWeightForm(request.POST, criteria_list = [i['name'] for i in request.session['criteria_list']])

        if carsCriteriaWeightForm.is_valid():
            criteria_list = request.session['criteria_list']
            for i in range(len(criteria_list)):
                '''
                Criteria list holds 3-tuples representing each criteria options.
                [0] = APIT's dictionary information about the criteria
                [1] = integer representing weight of criteria
                [2] = auto-scoring option
                '''
                criteria_list[i] = (criteria_list[i],carsCriteriaWeightForm.cleaned_data[str(i)],0)

            request.session['criteria_list'] = criteria_list

            return HttpResponseRedirect('/cars/auto_scores/')
    else:
        carsCriteriaWeightForm = CarsCriteriaWeightForm(criteria_list = [i['name'] for i in request.session['criteria_list']])

    return render(request, 'cars/cars_criteria_weight.html', {"carsCriteriaWeightForm" : carsCriteriaWeightForm})

def cars_auto_scores(request):
    if request.method=='POST':
        carsAutoScoreForm = CarsAutoScoreForm(request.POST, criteria_list = [i[0] for i in request.session['criteria_list']])

        if carsAutoScoreForm.is_valid():
            criteria_list = request.session['criteria_list']
            for i in range(len(criteria_list)):
                criteria_list[i] = (criteria_list[i][0], criteria_list[i][1], carsAutoScoreForm.cleaned_data[str(i)])

            request.session['criteria_list'] = criteria_list

            return HttpResponseRedirect('/cars/scores/')

    else:
        carsAutoScoreForm = CarsAutoScoreForm(criteria_list = [i[0] for i in request.session['criteria_list']])

    return render(request, 'cars/cars_auto_scores.html', {"carsAutoScoreForm" : carsAutoScoreForm})

def auto_scorer(num,max,min,asc):
    #If max = min then there is only one option and therefore the only option is the best
    if max==min:
        return 100
    if asc:
        return ((100*(num-min))/(max-min))
    else:
        return((100*(max-num))/(max-min))

def cars_scores(request):
    if request.method == 'POST':
        carsScoreForm = CarsScoreForm(request.POST,the_option_list=request.session['option_list'])

        if carsScoreForm.is_valid():
            #The next section of code takes the scores the user inputted and assigns them
            #to any item that fits that score.
            weighted_scores = []
            for i in range(len(request.session['option_list'])):
                weighted_scores.append(((carsScoreForm.cleaned_data[str(i)])*(request.session['criteria_list'][request.session['remaining']][1]),request.session['option_list'][i][1]))

            carss = request.session['carss']

            for key, value in carss.items():
                for i in range(len(weighted_scores)):
                    if value[1] == weighted_scores[i][1]:
                        new_score = value[2] + weighted_scores[i][0]
                        carss[key] = (carss[key][0], carss[key][1], new_score)

            request.session['carss'] = carss

            if request.session['remaining'] > 0:
                cont = True
                while cont and request.session['remaining'] > 0:
                    option_list = []
                    '''
                    Criteria is a 3-tuple representing a criteria option.
                    [0] = APIT's dictionary information about the criteria
                    [1] = integer representing weight of criteria
                    [2] = auto-scoring option
                    '''
                    criteria = request.session['criteria_list'][request.session['remaining']-1]
                    '''
                        Option list stores all the possible values for every criteria.
                        Each cars in carss stores the index of its criteria option in the option list.
                    '''
                    for key, value in carss.items():
                        if 'api_variable2' in criteria[0]:
                            if value[0][criteria[0]['api_variable']][criteria[0]['api_variable2']] in option_list:
                                carss[key] = (carss[key][0],option_list.index(value[0][criteria[0]['api_variable']][criteria[0]['api_variable2']]),carss[key][2])
                            else:
                                option_list.append(value[0][criteria[0]['api_variable']][criteria[0]['api_variable2']])
                                carss[key] = (carss[key][0],len(option_list) - 1,carss[key][2])
                        else:
                            if value[0][criteria[0]['api_variable']] in option_list:
                                carss[key] = (carss[key][0],option_list.index(value[0][criteria[0]['api_variable']]),carss[key][2])
                            else:
                                option_list.append(value[0][criteria[0]['api_variable']])
                                carss[key] = (carss[key][0],len(option_list) - 1,carss[key][2])


                    for i in range(0,len(option_list)):
                        option_list[i] = (option_list[i], i)

                    option_list = sorted(option_list, key=lambda x: (x[0] is None, x[0]))

                    if criteria[2] != 2:
                        min = option_list[0][0]
                        if option_list[-1][0] == None:
                            max = option_list[-2][0]
                        else:
                            max = option_list[-1][0]

                        for i in range(len(option_list)):
                            if option_list[i][0] == None:
                                option_list[i] = (0,option_list[i][1])
                            else:
                                option_list[i] = (auto_scorer(option_list[i][0],max,min,criteria[2]==0),option_list[i][1])

                        for key, value in carss.items():
                            for i in range(len(option_list)):
                                if value[1] == option_list[i][1]:
                                    new_score = value[2] + (option_list[i][0]*request.session['criteria_list'][request.session['remaining']-1][1])
                                    carss[key] = (carss[key][0], carss[key][1], new_score)

                        request.session['remaining'] = request.session['remaining'] - 1
                        request.session['carss'] = carss

                    else:
                        cont = False
                        request.session['carss'] = carss

                        option_list_names = []
                        for option in option_list:
                            if criteria[0]["needs_table"]:
                                option_list_names.append(criteria[0]["table"][option[0]])
                            else:
                                option_list_names.append(option[0])

                        carsScoreForm = CarsScoreForm(the_option_list=option_list_names)

                if request.session['remaining'] <= 0:
                    return HttpResponseRedirect('/cars/results/')


                request.session['carss'] = carss
                request.session['option_list'] = option_list
                request.session['remaining'] = request.session['remaining'] - 1

            else:
                return HttpResponseRedirect('/cars/results/')

    else:
        request.session['remaining'] = len(request.session['criteria_list'])
        print(request.session['decision'].params)
        cars_info_list = request.session['decision'].pull()

        '''
            carss is a dictionary with all the cars information and their scores.
            The keys are the school names and the values are a tuple:
            cars[0] = the json object with all the cars information
            cars[1] = is the index for the cars's score for the current criteria being scored in option_list
            cars[2] = the cars's current score with the criteria already scored
        '''
        carss = {}
        for cars in cars_info_list:
            carss[cars['cars']['name']] = (cars['cars'], 0, 0)

        cont = True

        while cont and request.session['remaining'] > 0:
            option_list = []
            '''
            Criteria is a 3-tuple representing a criteria option.
            [0] = APIT's dictionary information about the criteria
            [1] = integer representing weight of criteria
            [2] = auto-scoring option
            '''
            criteria = request.session['criteria_list'][request.session['remaining']-1]

            '''
                Option list stores all the possible values for every criteria.
                Each cars in carss stores the index of its criteria option in the option list.
            '''
            for key, value in carss.items():
                if 'api_variable2' in criteria[0]:
                    if value[0][criteria[0]['api_variable']][criteria[0]['api_variable2']] in option_list:
                        carss[key] = (carss[key][0],option_list.index(value[0][criteria[0]['api_variable']][criteria[0]['api_variable2']]),carss[key][2])
                    else:
                        option_list.append(value[0][criteria[0]['api_variable']][criteria[0]['api_variable2']])
                        carss[key] = (carss[key][0],len(option_list) - 1,carss[key][2])
                else:
                    if value[0][criteria[0]['api_variable']] in option_list:
                        carss[key] = (carss[key][0],option_list.index(value[0][criteria[0]['api_variable']]),carss[key][2])
                    else:
                        option_list.append(value[0][criteria[0]['api_variable']])
                        carss[key] = (carss[key][0],len(option_list) - 1,carss[key][2])

            for i in range(0,len(option_list)):
                option_list[i] = (option_list[i], i)

            option_list = sorted(option_list, key=lambda x: (x[0] is None, x[0]))

            if criteria[2] != 2:
                min = option_list[0][0]
                if option_list[-1][0] == None:
                    max = option_list[-2][0]
                else:
                    max = option_list[-1][0]

                for i in range(len(option_list)):
                    if option_list[i][0] == None:
                        option_list[i] = (0,option_list[i][1])
                    else:
                        option_list[i] = (auto_scorer(option_list[i][0],max,min,criteria[2]==0),option_list[i][1])

                for key, value in carss.items():
                    for i in range(len(option_list)):
                        if value[1] == option_list[i][1]:
                            new_score = value[2] + (option_list[i][0]*request.session['criteria_list'][request.session['remaining']-1][1])
                            carss[key] = (carss[key][0], carss[key][1], new_score)

                request.session['remaining'] = request.session['remaining'] - 1
                request.session['carss'] = carss
            else:
                cont = False
                request.session['carss'] = carss

                option_list_names = []
                for option in option_list:
                    if criteria[0]["needs_table"]:
                        option_list_names.append(criteria[0]["table"][option[0]])
                    else:
                        option_list_names.append(option[0])

                carsScoreForm = CarsScoreForm(the_option_list=option_list_names)

        if request.session['remaining'] <= 0:
            return HttpResponseRedirect('/carss/results/')

        request.session['carss'] = carss
        request.session['option_list'] = option_list
        request.session['remaining'] = request.session['remaining'] - 1

    return render(request, 'cars/cars_scores.html', {"carsScoreForm" : carsScoreForm, "criteria_name" : criteria[0]['name'], "criteria_units" : criteria[0]["units"]})

def cars_results(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        profile = UserProfile.objects.get(user=user)
        newDecision = Decide(user_profile = profile, decisionName = "cars")
        newDecision.save()

        carsList = request.session['carss']
        criteriaList = request.session['criteria_list']

        for cars in carsList:
            newItem = Item(itemName = cars[0], itemScore = cars[1], decision = newDecision)
            newItem.save()
        for criteria in criteriaList:
            newCriteria = Criteria(criteriaName = criteria[0]['name'], criteriaWeight = criteria[1], decision = newDecision)
            newCriteria.save()

        request.session['saved'] = True

    else:
        request.session['saved'] = False
        carsList = []

        for key,value in request.session['carss'].items():
            carsList.append((key,(round((value[2]/100),2))))

        carsList = sorted(carsList, key = lambda x: x[1],reverse=True)

        request.session['carss'] = carsList

    return render(request, 'cars/results.html', {"request" : request, "carsList" : carsList, "length" : len(carsList)})
