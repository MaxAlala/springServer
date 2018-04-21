from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from snippets import views
from snippets.views import RegisterUserView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^register2/$', views.CreateUserView.as_view(), name='user'),
    url(r'^', include(router.urls)),
    url(r'^register/$', view=RegisterUserView.as_view(), name='register'),
]
