from django import forms

class MovieCriteriaForm(forms.Form):
	def __init__(self, *args, **vargs):
		super(CollegeCriteriaForm,self).__init__(*args,**vargs)
		for i in range(len(APIT)):
			field = forms.BooleanField(label=APIT[i]['name'],required=False)
			self.fields[str(i)] = field

class MovieCriteriaWeightForm(forms.Form):
    def __init__(self, *args, **vargs):
        criteria_list = vargs.pop('criteria_list')
        super(CollegeCriteriaWeightForm,self).__init__(*args,**vargs)
        for i in range(len(criteria_list)):
                field = forms.IntegerField(label=criteria_list[i],
                                        widget=forms.HiddenInput(attrs={
                                            'id':('weight_' + str(i))
                                            }))
                self.fields[str(i)] = field


AUTO_CHOICES = [(0, "Higher Values = Better Scores"),(1, "Lower Values = Better Scores")]

class MovieAutoScoreForm(forms.Form):
    def __init__(self, *args, **vargs):
        criteria_list = vargs.pop('criteria_list')
        super(CollegeAutoScoreForm,self).__init__(*args,**vargs)
        for i in range(len(criteria_list)):
                field = forms.IntegerField(label=criteria_list[i]['name'],
                                        widget=forms.Select(attrs={'class': 'form-control'},choices=AUTO_CHOICES))
                self.fields[str(i)] = field
