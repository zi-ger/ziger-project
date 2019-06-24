from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

User = get_user_model()

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def EditProfile(request):
  if request.method == 'POST':
    form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)

    if form.is_valid():
      form.save()
      return redirect('index')
  else:
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
