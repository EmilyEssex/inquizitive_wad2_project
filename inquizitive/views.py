from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.forms import formset_factory 
from .forms import SignUpForm, EditProfileForm, AddAQuestionForm 
from inquizitive.forms import CreateAQuizForm,  AddAQuestionForm
from .models import Quiz, Question
from django.urls import reverse
 

# Create your views here.


def home(request): 
    #everything before render is new -Hana
    quizzes_list = Quiz.objects.all()
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['quizzes'] = quizzes_list
    return render(request, 'inquizitive/home.html', context_dict)


def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Login Successful'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'inquizitive/login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request,('You are now logged out'))
	return redirect('home')


def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'inquizitive/register.html', context)


def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information 
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'inquizitive/edit_profile.html', context)
	

def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		#passes in user information 
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'inquizitive/change_password.html', context)


 
def creating_quiz(request): 
    user=request.user
    form = CreateAQuizForm()
    if request.method == 'POST':
        form = CreateAQuizForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('home')) ### not sure about this
        else:
            form=CreateAQuizForm()
    context = {'form': form}
    return render(request, 'inquizitive/creating_quiz.html', context)

 
def adding_questions(request, quiz_name_slug): 
    try:
        quiz = Quiz.objects.get(slug=quiz_name_slug) 
    except Quiz.DoesNotExist:
        quiz=None
    if quiz is None:
        return redirect('/inquizitive/creating_quiz/')

    form = AddAQuestionForm()
    if request.method == 'POST':
        form =  AddAQuestionForm(request.POST)
        if form.is_valid(): 
            if quiz:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
                redirect(reverse('show_quiz1', kwargs={'quiz_name_slug': quiz_name_slug}))
        else: 
            print(form.errors)

    context = {'form': form, 'quiz':quiz}

    QuestionFormSet = formset_factory(AddAQuestionForm, extra = 2)
    formset = QuestionFormSet(request.POST or None)
    
    if formset.is_valid():
        for form in formset:
            if form.is_valid(): 
                if quiz:
                    question = form.save(commit=False)
                    question.quiz = quiz
                    question.save()
                    redirect(reverse('show_quiz1', kwargs={'quiz_name_slug': quiz_name_slug}))
            else: 
                print(form.errors)

            
    context['formset'] = formset

    return render(request, 'inquizitive/adding_questions.html', context)

 
    #chnaged from quiz_name_slug
def show_quiz1(request, quiz_name_slug):
    context_dict = {}
    try:
# Can we find a category name slug with the given name?
# If we can't, the .get() method raises a DoesNotExist exception.
# The .get() method returns one model instance or raises an exception. 
        quiz = Quiz.objects.get(slug=quiz_name_slug)
        context_dict['quizName'] = quiz.quizName
       # quiz = Quiz.objects.get(slug=quiz_name_slug)
         
# Retrieve all of the associated pages.
# The filter() will return a list of page objects or an empty list. 
        questions = Question.objects.filter(quiz=quiz)
        # Adds our results list to the template context under name pages.
        context_dict['questions'] = questions
# We also add the category object from
# the database to the context dictionary.
# We'll use this in the template to verify that the category exists. 
        context_dict['quiz'] = quiz
      #  listQue=["a"]*quiz.numOfQue
        context_dict['numOfQue']= quiz.numOfQue
    except Quiz.DoesNotExist:
# We get here if we didn't find the specified category.
# Don't do anything -
# the template will display the "no category" message for us. 
        context_dict['category'] = None
        context_dict['questions'] = None
    # Go render the response and return it to the client.
    return render(request, 'inquizitive/quiz.html', context=context_dict)

 















