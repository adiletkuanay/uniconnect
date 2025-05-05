from django.shortcuts import redirect
from django.contrib import messages
from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """
        Override the default redirect after login to go to dashboard
        """
        return '/dashboard/'

    def is_open_for_signup(self, request):
        """
        Whether to allow sign up or not
        """
        return True

    def pre_login(self, request, user, **kwargs):
        """
        Perform any actions before the user is logged in
        """
        return super().pre_login(request, user, **kwargs)

    def login(self, request, user):
        """
        Perform the login action
        """
        super().login(request, user)

    def get_signup_redirect_url(self, request):
        """
        Override the default redirect after signup to go to dashboard
        """
        return '/dashboard/' 