from django.urls import path

from .views import ListMenusPageView, FoldersPageView

app_name = 'menu'

urlpatterns = [
    path('', ListMenusPageView.as_view(), name='list_menus'),
    path('<slug:menu_slug>/', FoldersPageView.as_view(), name='menu'),
]
