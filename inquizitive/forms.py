from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms 
import json
from inquizitive.models import Quiz, Question
from django.forms import formset_factory
from django.contrib.postgres.fields.jsonb import JSONField

#from splitjson.widgets import SplitJSONWidget
 

# default maximum number of forms in a formset, to prevent memory exhaustion
DEFAULT_MAX_NUM = 1000

class EditProfileForm(UserChangeForm):
	
	password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = User
		#excludes private information from User
		fields = ('username', 'first_name', 'last_name', 'email','password',)




class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), )
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

	def __init__(self, *args, **kwargs):
	    super(SignUpForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    self.fields['username'].widget.attrs['placeholder'] = 'User Name'
	    self.fields['username'].label = ''
	    self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer.</small></span>'

	    self.fields['password1'].widget.attrs['class'] = 'form-control'
	    self.fields['password1'].widget.attrs['placeholder'] = 'Password'
	    self.fields['password1'].label = ''
	    self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password must contain at least 8 characters.</li><li>Password can\'t be completely numeric.</li></ul>'

	    self.fields['password2'].widget.attrs['class'] = 'form-control'
	    self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
	    self.fields['password2'].label = ''
	    self.fields['password2'].help_text = '<span class="form-text text-muted"><small></small></span>'

 
 
DIFFICULTY_CHOICES=[
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
    ]
#form for quiz model
class CreateAQuizForm(forms.ModelForm):
    quizName = forms.CharField(max_length=500, help_text="Quiz Name: ")
    quizSubject = forms.CharField(max_length=500, help_text="Quiz Subject: ")
    quizDifficulty=forms.CharField(label='Quiz Difficulty: ', widget=forms.Select(choices=DIFFICULTY_CHOICES))
    numOfQue=forms.IntegerField(max_value=100, min_value=0, help_text="Number of questions in quiz ")
    passcode = forms.CharField(max_length=500, help_text="Passcode",label='', required=False)
    class Meta:
        model = Quiz
        fields = ('quizName', 'quizSubject', 'quizDifficulty','numOfQue', "user", 'passcode' )

#form for question model
class AddAQuestionForm(forms.ModelForm):
   
    questionText = forms.CharField(max_length=500, help_text="Question: ",label='',required=True)
    questionMarks = forms.IntegerField(max_value=100, min_value=0,label='')
    #answers = JSONField()
    optiona = forms.CharField(max_length=500, help_text="Answer A",label='')
    optionb = forms.CharField(max_length=500, help_text="Answer B",label='')
    optionc = forms.CharField(max_length=500, help_text="Answer C",label='')
    optiond = forms.CharField(max_length=500, help_text="Answer D",label='')
    correctAnswer=forms.CharField(max_length=500, help_text="Enter answer (copy and paste please)",label='')
    
   # attrs = {'class': 'special', 'size': '40'}
   # data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
    class Meta:
        model = Question
        fields = ('questionText',  'questionMarks', 'optiona' , 'optionb', 'optionc', 'optiond', 'correctAnswer')
   # we should add the ansers as well
   
   
   
 #Removing this form doesnt affect the app   
 
class TakeQuizForm(forms.ModelForm):
   
    questionText = forms.CharField(max_length=500, help_text="Question: ")
    questionMarks = forms.IntegerField(max_value=100, min_value=0)
    #answers = JSONField()
    optionA  = forms.CharField(max_length=500, help_text="Answer A")
    optionb = forms.CharField(max_length=500, help_text="Answer B")
    optionc = forms.CharField(max_length=500, help_text="Answer C")
    optiond = forms.CharField(max_length=500, help_text="Answer D")
    correctAnswer=forms.CharField(max_length=500, help_text="Enter answer (copy and paste please)")
   # attrs = {'class': 'special', 'size': '40'}
   # data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
    class Meta:
        model = Question
        fields = ('questionText',  'questionMarks', 'optiona' , 'optionb', 'optionc', 'optiond', 'correctAnswer')
   # we should add the ansers as well
   
    
 
 
   
   
   
   
   
   
   
   
   
   
   
   
   