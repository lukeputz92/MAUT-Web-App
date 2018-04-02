from django import forms

def MovieCriteriaForm(forms.Form):
	year = institution_level = forms.BooleanField(required=False,label="Year of Release")
	IMDBscore = institution_level = forms.BooleanField(required=False,label="IMDB Score")

class CollegeCriteriaWeightForm(forms.Form):
    def __init__(self, *args, **vargs):
        criteria_list = vargs.pop('criteria_list')
        super(CollegeCriteriaWeightForm,self).__init__(*args,**vargs)
        for i in range(len(criteria_list)):
                field = forms.IntegerField(label=criteria_list[i],
                                        widget=forms.HiddenInput(attrs={
                                            'id':('weight_' + str(i))
                                            }))
                self.fields[str(i)] = field