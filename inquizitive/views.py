from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm 
from inquizitive.forms import CreateAQuizForm,  AddAQuestionForm
from django.shortcuts import redirect
from .models import Quiz, Question
from django.urls import reverse
from datetime import datetime
 

# Create your views here.


def home(request): 
    #everything before render is new -Hana
    quizzes_list = Quiz.objects.all()
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['quizzes'] = quizzes_list
    request.session.set_test_cookie()
      # Obtain our Response object early so we can add cookie information.
    response = render(request, 'inquizitive/home.html', context_dict)
      # Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    # Return response back to the user, updating any cookies that need changed.
    return response
    #return render(request, 'inquizitive/home.html', context_dict)

# A helper method
def get_server_side_cookie(request, cookie, default_val=None): 
    val = request.session.get(cookie)
    if not val:
        val = default_val 
    return val
# Updated the function definition
def visitor_cookie_handler(request ):
    visits = int(get_server_side_cookie(request, 'visits', '1')) 
    last_visit_cookie = get_server_side_cookie(request, 'last_visit',  str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
     
    if (datetime.now() - last_visit_time).seconds > 3600:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count 
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie 
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits


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
    visitor_cookie_handler(request)
   
    context = {'form': form,'visits':request.session['visits']}
   # context['visits'] = request.session['visits']
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
    
    return render(request, 'inquizitive/adding_questions.html', context)

 
 
def show_quiz1(request, quiz_name_slug):
    if request.session.test_cookie_worked(): 
        print("TEST COOKIE WORKED!") 
        request.session.delete_test_cookie()
        
        
    context_dict = {}
    try:
        quiz = Quiz.objects.get(slug=quiz_name_slug)
        context_dict['quizName'] = quiz.quizName
        questions = Question.objects.filter(quiz=quiz)
        context_dict['questions'] = questions
        context_dict['quiz'] = quiz
        context_dict['numOfQue']= quiz.numOfQue
        context_dict['optionsList']=[Question.optiona,Question.optionb,Question.optionc,Question.optiond]
        score =0
        maxPossibleScore=0
        for q in questions:
            maxPossibleScore+=q.questionMarks
            
        
        
    except Quiz.DoesNotExist:
 
        context_dict['category'] = None
        context_dict['questions'] = None
    # Go render the response and return it to the client.

    return render(request, 'inquizitive/quiz.html', context=context_dict)

 















