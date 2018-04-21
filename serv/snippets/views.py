from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
# from rest_framework.permissions import AllowAny
from snippets.serializers import SnippetSerializer, UserSerializer

from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic import CreateView
from snippets.forms import RegisterUserForm
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView
class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "account/register.html"

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated():
        #     return HttpResponseForbidden()

        return super(RegisterUserView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return HttpResponse('User registered')

# from django.contrib.auth.models import User
# user = User.objects.create_user(username='Greta',
#                                  email='jlennon@beatles.com',
#                                  password='glass onion')

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly, )

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer

# -*- coding: utf-8 -*


# class LoginUserView(LoginView):
#     form_class = LoginForm
#     template_name = "account/login.html"
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('dashboard')
#
#
# @method_decorator(login_required, name='dispatch')
# class DashboardView(TemplateView):
#     template_name = 'account/dashboard.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         return super(DashboardView, self).dispatch(request, *args, **kwargs)
