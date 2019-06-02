from django.urls import path
from . import views

urlpatterns = [
    path('<status>/<lat>/<lon>', views.index, name='index'),
    path('', views.default, name='default'),
]

# push git
