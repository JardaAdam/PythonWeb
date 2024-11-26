from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Přesměrování na login po úspěšné registraci
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

