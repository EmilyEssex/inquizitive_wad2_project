from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms 

from inquizitive.models import Quiz, Question



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
    name = forms.CharField(max_length=500, help_text="Please enter the name of your quiz.")
    subject = forms.CharField(max_length=500, help_text="Please enter the subject of your quiz")
    difficulty=forms.CharField(label='What is the difficult level of the quiz', widget=forms.Select(choices=DIFFICULTY_CHOICES))
    class Meta:
        model = Quiz
        fields = ('name', 'subject', 'difficulty')

#form for question model
class AddAQuestionForm(forms.ModelForm):
    questionText = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    questionMarks = forms.IntegerField(max_value=100, min_value=1)
    class Meta:	
        model = Question
        fields = ('questionText',  'questionMarks')
   # we should add the ansers as well
 
 
          
        
        
        
        
        
        