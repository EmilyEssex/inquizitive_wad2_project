from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm 
from inquizitive.forms import CreateAQuizForm,  AddAQuestionForm
from django.shortcuts import redirect


# Create your views here.


def home(request): 
	return render(request, 'inquizitive/home.html', {})


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
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database. 
            form.save(commit=True)
            # Now that the category is saved, we could confirm this. 
            # For now, just redirect the user back to the index view. 
            return redirect('/inquizitive/adding_questions') ### not sure about this
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            form=CreateAQuizForm()
    # Will handle the bad form, new form, or no form supplied cases. # Render the form with error messages (if any).
    context = {'form': form}
    return render(request, 'inquizitive/creating_quiz.html', context)

 
def adding_questions(request): 
    user=request.user
    form = AddAQuestionForm()
    if request.method == 'POST':
        form = AddAQuestionForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database. 
            form.save(commit=True)
            # Now that the category is saved, we could confirm this. 
            # For now, just redirect the user back to the index view. 
            return redirect('add a question') ### not sure about this
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            form=AddAQuestionForm()
    # Will handle the bad form, new form, or no form supplied cases. # Render the form with error messages (if any).
    context = {'form': form}
    return render(request, 'inquizitive/adding_questions.html', context)
 
 