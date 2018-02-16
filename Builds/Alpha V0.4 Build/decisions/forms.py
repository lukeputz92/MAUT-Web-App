from django import forms
from decisions.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.formsets import formset_factory, BaseFormSet

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model= User
		fields = (
		'username',
		'first_name',
		'last_name',
		'email',
		'password1',
		'password2'
		)
	def save(self, commit=True):
		user=super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']


class EditProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields = (
		'first_name',
		'last_name',
		'email',
		'password'
		)


class ItemForm(forms.Form):

	item_name = forms.CharField(
							max_length=100,
							widget=forms.TextInput())

class BaseItemFormSet(BaseFormSet):
	def __init__(self, *args, **kwargs):
		super(BaseItemFormSet, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False

	def clean(self):
		#Check if any of the individual forms have errors.
		#If so then return because there is no point in checking for more errors.
		if any(self.errors):
			return

		#Check to see if there are at least 2 items to decide between
		if self.data['form-TOTAL_FORMS'] < '2':
			raise forms.ValidationError('There must be at least 2 items to decide between.')


class CriteriaForm(forms.Form):
	criteria_name = forms.CharField(
							max_length=100,
							widget=forms.TextInput())
	criteria_weight = forms.IntegerField(widget=forms.TextInput(attrs={
										'onblur' : 'calculate()',
										}))

class BaseCriteriaFormSet(BaseFormSet):
	def __init__(self, *args, **kwargs):
		super(BaseCriteriaFormSet, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False

	def clean(self):
		#Check if any of the individual forms have errors.
		#If so then return because there is no point in checking for more errors.
		if any(self.errors):
			return

		#Checking all the weights for valid data
		weight = 0
		for form in self.forms:
			if form.cleaned_data:
				tempWeight = form.cleaned_data['criteria_weight']
				#Checks if each individual weight is between 1 and 100.
				if tempWeight > 100 or tempWeight <=0:
					raise forms.ValidationError(
						('Invalid weight submitted. ' + str(tempWeight) + ' is not between 1-100'),
						code = 'invalid_weight'
						)
				else:
					weight += tempWeight
		#Checks the sum of all the weights to make sure it is 100
		if weight != 100:
			raise forms.ValidationError(
				'All the criteria weights must sum to 100',
				code = 'invalid_weight_sum'
				)


'''
Form that only takes as input the name of the user's decision.
'''
class DecideForm(forms.Form):
	yourDecision = forms.CharField(label = 'What are you deciding on?', max_length=100)


'''
This is the form for the scores of each item based on each criteria.
This form is dynamic and takes as input arguments called criteria_count and item_count.

Ex: myform = ScoreForm(criteria_count = 8, item_count = 4)

Each element is stored in the fields dictionary with the key ITEMINDEX_CRITERIAINDEX.
'''
class ScoreForm(forms.Form):
	def __init__(self, *args, **vargs):
		#Popping the criteria_count and item_count variables before calling the parent's constructor
		criteria_count = vargs.pop('criteria_count')
		item_count = vargs.pop('item_count')
		super(ScoreForm,self).__init__(*args,**vargs)
		for i in range(0,item_count):
			for j in range(0,criteria_count):
				field = forms.IntegerField()
				self.fields[str(i) + '_' + str(j)] = field

	def clean(self):
		#check to make sure each score is between 0 and 100
		if self.cleaned_data:
			for key in self.cleaned_data:
				if self.cleaned_data[key] > 100 or self.cleaned_data[key] < 0:
					raise forms.ValidationError(('Invalid Score Submitted. ' + str(self.cleaned_data[key]) + ' is not between 0 and 100'))


#The Criteria and Item formsets are defined here so it doesn't have to be done in the view
CriteriaFormSet = formset_factory(CriteriaForm,min_num=1,extra=0,formset=BaseCriteriaFormSet)
ItemFormSet = formset_factory(ItemForm,min_num=1,extra=0,formset=BaseItemFormSet)

#All the information used in the 'Contact Us' page.
class ContactForm(forms.Form):
    contact_name = forms.CharField(label = "Name",required=True,
    							widget = forms.TextInput(attrs={
								'placeholder':'Name'
								}))
    contact_email = forms.EmailField(label = "Email",required=False,
    							widget = forms.TextInput(attrs={
    								'placeholder': 'Email (optional)'
    								}))
    content = forms.CharField(label = "Message",
        required=True,
        widget=forms.Textarea(attrs={
        						'placeholder': 'Message'
        					  })
    )