"""
URL configuration for bt_live project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.urls import path

from . import stream
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.data, name='data'),
    path('msg', stream.msg, name='msg'),
    path('favicon.png', views.favicon_png, name='favicon_png'),
    path('favicon.svg', views.favicon_svg, name='favicon_svg'),
]
