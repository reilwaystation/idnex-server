from django.urls import path, include
from .views import signup, verify, signin, currentuser, resend, recover, reset, change, googleauth, signout, facebookauth, update

urlpatterns = [
    path('signup', signup),
    path('signin', signin, name='signin'),
    path('signout', signout, name='signout'),
    path('google', googleauth, name='googleauth'),
    path('facebook', facebookauth, name='facebookauth'),
    path('resend', resend, name='resend'),
    path('verify', verify, name="verify"),
    path('recover', recover, name='recover'),
    path('reset', reset, name='reset'),
    path('currentuser', currentuser, name='currentuser'),
    path('update', update, name="update"),
    path('change', change, name='change'),
]
