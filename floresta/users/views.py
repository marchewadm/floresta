from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from store.views import get_message
from .forms import SignUpForm


def signin(request):
    if request.user.is_authenticated:
        request.session['message'] = "Jesteś już zalogowany"
        return redirect("/")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            request.session['message'] = "Coś poszło nie tak..."
            return redirect("/signin/")
    else:
        context = {}
        context.update(get_message(request))

        return render(request, 'users/signin.html', context)


def signup(request):
    if request.user.is_authenticated:
        request.session['message'] = "Jesteś już zalogowany"
        return redirect("/")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                request.session['message'] = "Rejestracja przebiegła pomyślnie!"
                return redirect("/")
            else:
                request.session['message'] = "Coś poszło nie tak..."
                return redirect("/signup/")
    else:
        form = SignUpForm()

    context = {'form': form}
    context.update(get_message(request))
    return render(request, 'users/signup.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        request.session['message'] = "Musisz być zalogowany, aby móc wykonać tę czynność"
        return redirect('/')

    logout(request)
    return redirect('/')
