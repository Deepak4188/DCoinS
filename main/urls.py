from django.urls import path
from . import views

urlpatterns = [
    path('mineBlock', views.mineBlock, name="mineBlock"),
    path('getChain', views.getChain, name="getChain"),
    path('isValid', views.isChainValid, name="isChainValid")
]