from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='list_menus'),
    path('<slug:menu_slug>/', views.FoldersPageView.as_view(), name='menu')
]
