from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not self.is_profile_complete(request.user):
            if request.path not in [reverse('users:profile'), reverse('users:logout')]:
                return redirect(reverse('users:profile'))
        response = self.get_response(request)
        return response

    def is_profile_complete(self, user):
        if hasattr(user, 'profile') and user.profile.phone_number:
            return True
        return False