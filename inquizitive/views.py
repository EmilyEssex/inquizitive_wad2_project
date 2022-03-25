from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm, UpdateImageForm
from inquizitive.forms import CreateAQuizForm,  AddAQuestionForm , TakeQuizForm
from django.shortcuts import redirect
from .models import Quiz, Question, UserProfile
from django.urls import reverse
from datetime import datetime
from django.forms import formset_factory 
import json 
from django.views import View
 
# Create your views here.


def home(request): 
    if 'search' in request.GET:
        q=request.GET['search']
        quizzes_list=Quiz.objects.filter(quizName__icontains=q)
    else:
        quizzes_list=Quiz.objects.all()
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['quizzes'] = quizzes_list
    request.session.set_test_cookie()
    request_user = request.user
    context_dict["request_user"]= request_user
    response = render(request, 'inquizitive/home.html', context_dict)
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return response

def get_server_side_cookie(request, cookie, default_val=None): 
    val = request.session.get(cookie)
    if not val:
        val = default_val 
    return val


def visitor_cookie_handler(request ):
    visits = int(get_server_side_cookie(request, 'visits', '1')) 
    last_visit_cookie = get_server_side_cookie(request, 'last_visit',  str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds > 3600:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits


def meet_the_team(request):
    print("meet_the_team")
    # quizzes_list=Quiz.objects.all()
    context_dict={}
    # context_dict['quizzes'] = quizzes_list
    return render(request, 'inquizitive/meet_the_team.html',context_dict)


def login_user (request):
	if request.method == 'POST':  
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None: 
			login(request, user)
			messages.success(request,('Login Successful'))
			return redirect('home') 
		else:
			messages.success(request,('Error logging in'))
			return redirect('login')  
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

@login_required
def user_account(request):
    print("user account")
    quizzes_list=Quiz.objects.all()
    context_dict={}
    context_dict['quizzes'] = quizzes_list
    return render(request, 'inquizitive/user_account.html',context_dict)

@login_required
def update_image(request):

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        image_form = UpdateImageForm(data=request.POST, instance=user_profile)

        if image_form.is_valid():
            profile = image_form.save(commit=False)

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
    else:
        image_form = UpdateImageForm(instance=user_profile)
    return render(request, 'inquizitive/update_image.html', {'update_image_form': image_form})


def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		 
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
	else: 		 
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
   
    return render(request, 'inquizitive/creating_quiz.html', context)

def meet_the_team(request): 
    return render(request, 'inquizitive/meet_the_team.html')

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
 
    context = {'form': form, 'quiz':quiz}

    QuestionFormSet = formset_factory(AddAQuestionForm, extra = quiz.numOfQue )
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

    
 

 
# View for editing the quiz - only creators could do that
def show_quiz1(request, quiz_name_slug):
    if request.session.test_cookie_worked(): 
        print("TEST COOKIE WORKED!") 
        request.session.delete_test_cookie()
        
        
    context_dict = {}
    try:
        #if request.method == 'POST':
            quiz = Quiz.objects.get(slug=quiz_name_slug)
            context_dict['quizName'] = quiz.quizName
            questions = Question.objects.filter(quiz=quiz)
            context_dict['questions'] = questions
            context_dict['quiz'] = quiz
            context_dict['numOfQue']= quiz.numOfQue
            context_dict['optionsList']=[Question.optiona,Question.optionb,Question.optionc,Question.optiond]
     
        
    except Quiz.DoesNotExist:
 
        context_dict['category'] = None
        context_dict['questions'] = None
    # Go render the response and return it to the client.

    return render(request, 'inquizitive/quiz.html', context=context_dict)

        
 
# This view handles both allowing the user to answer and displaying the results
# The above results view could be removed 
def answerQuiz(request, quiz_name_slug):
    quiz = Quiz.objects.get(slug=quiz_name_slug)
    #print("mmmm",quiz.quizSubject)
    #quiz.process_likes()
   # quiz.save()
    #likes=quiz.likes
   # print(likes)
    if request.method == 'POST':
        print(request.POST)
        questions = Question.objects.filter(quiz=quiz)
        score=0
        total=0
        
        for question in questions:
            total+=question.questionMarks
            print(request.POST.get(str(question.questionText)))
            print(question.correctAnswer)
            print()
            if question.correctAnswer ==  request.POST.get(question.questionText):
                score+=question.questionMarks
                
        if total!=0:    
            percent = score/(total) *100
        else:
            percent=0
        
        context = {
           # 'time': request.POST.get('timer'),
            'percent':percent, 'subject':quiz.quizSubject, 'difficulty':quiz.quizDifficulty
        }
        return render(request,'inquizitive/quizResults.html',context)
    else:
            
            context_dict = {}
            quiz = Quiz.objects.get(slug=quiz_name_slug)
            # print("passcode" )
            # print( quiz.passcode)
            # print(request.POST.get('password'))
            context_dict['quizName'] = quiz.quizName
            #context_dict['likes'] = likes
            questions = Question.objects.filter(quiz=quiz)
            context_dict['questions'] = questions
            context_dict['quiz'] = quiz
            context_dict['numOfQue']= quiz.numOfQue
           
            context_dict['optionsList']=Question.optionsList
            #[Question.optiona,Question.optionb,Question.optionc,Question.optiond]
            if request.POST.get("quiz_id"):
                quiz.like.add(request.user)
                context_dict['liked']="We're happy you enjoyed this quiz!"
            else: context_dict['liked']="jjj"
                
            context_dict['correctAnswer']=Question.correctAnswer
 
            return render(request, 'inquizitive/answerQuiz.html', context_dict) 



def likeQuiz(request, pk):
    quiz= get_object_or_404(Quiz, id=request.POST.get("quiz_id"))
    quiz.like.add(request.user)
    return HttpResponseRedirect(reverse("answerQuiz", args=[str(pk)]))


