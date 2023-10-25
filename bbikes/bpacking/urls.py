from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page
from rest_framework import routers


from .views import *

# class MyCustomRouter(routers.SimpleRouter):
#     routes = [
#         routers.Route(url=r'^{prefix}$',
#                       mapping={'get': 'list'},
#                       name='{basename}-list',
#                       detail=False,
#                       initkwargs={'suffix': 'List'}),
#         routers.Route(url=r'^{prefix}/{lookup}$',
#                       mapping={'get': 'retrieve'},
#                       name='{basename}-detail',
#                       detail=True,
#                       initkwargs={'suffix': 'Detail'})
#     ]

router = routers.DefaultRouter()
router.register(r'bikes', BikesViewSet, basename='bikes')
# print(router.urls)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),

    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('edit/<slug:slug>/', UpdatePage.as_view(), name='edit_page'),

    path('category/<slug:cat_slug>/', BikeCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', BikeTags.as_view(), name='tag'),
    path('profile/', Profile.as_view(), name='profile'),

    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="bpacking/password_change_done.html"), name='password_change_done'),

    path('api/v1/', include(router.urls)),  #http://127.0.0.1:8000/api/v1/bikes/

]