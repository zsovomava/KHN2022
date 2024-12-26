from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {
        'object': user
    }
    if user == request.user:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            p_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=user.profile)
            if 'delete' in request.POST:
                return redirect('delete')
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(
                    request, 'A kért módosítások sikeresen végrehajtódtak.')
                return redirect('profile', pk=user.id)
        else:
            u_form = UserUpdateForm(instance=user)
            p_form = ProfileUpdateForm(instance=user.profile)
        context['u_form'] = u_form
        context['p_form'] = p_form
    return render(request, 'accounts/profile.html', context)


@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('main:home')
    return render(request, 'accounts/user_confirm_delete.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'A fiók létrejött.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
