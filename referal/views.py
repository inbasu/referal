from django.shortcuts import redirect, render
from .models import validate_this

# Create your views here.


def register_referal(request):
    """
    This is mock function
    In real project use user auth system
    """
    ...


class InviteView:
    """
    Invite Referal with POST request
    In inheret class reassingt 'redirect_page'
    """

    redirect_page: str

    def invite_referal(self, request):
        """Request must contain invite code"""
        invite_code = request.POST["invite_code"]
        if validate_this(invite_code):
            request.user.invite()
        return redirect(self.redirect_page)

    def post(self, request, *args, **kwargs):
        self.invite_referal(request)
