from django.conf.urls import url,include

from website.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()



urlpatterns = [

]
urlpatterns += router.urls
