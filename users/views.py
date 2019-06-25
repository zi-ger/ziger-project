from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
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
      messages.success(request, 'Profile updated.')
      return redirect('/u/{}'.format(request.user.username))
    else:
      messages.warning(request, 'Not valid form.')
      return redirect('/u/{}'.format(request.user.username))

  else:
    form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
