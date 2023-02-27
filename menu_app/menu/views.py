from collections import defaultdict

from django.db.models import Q
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from .models import Menu, Folder


class ListMenusPageView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Render start page with list of menus.
        """
        menus = Menu.objects.all()
        return render(request, 'list_menus.html', {'menus': menus})


class FoldersPageView(View):
    MAIN_NODE = 'root'

    @staticmethod
    def clean_path_nodes(path: list[str]) -> dict[str, str]:
        """
        Make dictionary with pairs (folder_slug, parent_folder_slug).
        For folders with no parent add 'root'.
        """
        path_nodes = {}
        for i in range(1, len(path)):

            # check circles in path
            if path[i] in path_nodes:
                raise Http404
            path_nodes[path[i]] = path[i-1]

        return path_nodes

    def get(self, request: HttpRequest, menu_slug: str) -> HttpResponse:
        """
        Render page with tree menu structure.
        """
        path_string = request.GET.get('path')
        path = [self.MAIN_NODE, ]
        path_nodes = {}
        parent_query = Q(parent=None)
        if path_string:
            parents_slugs = path_string.strip('/').split('/')
            path += parents_slugs
            path_nodes = self.clean_path_nodes(path)
            parent_query = parent_query | Q(parent__slug__in=parents_slugs)

        folders = Folder.objects.filter(
            Q(menu__slug=menu_slug) & parent_query).select_related('parent')

        folder_nodes = defaultdict(list)
        for folder in folders:
            folder_parent = self.MAIN_NODE
            if folder.parent:
                folder_parent = folder.parent.slug

            # check correct folder - parent_folder link
            if path_nodes.get(folder.slug, folder_parent) != folder_parent:
                raise Http404
            folder_nodes[folder_parent].append(folder)

        context = {
            'path': path,
            'folder_nodes': folder_nodes,
            'menu_slug': menu_slug,
        }

        return render(request, 'menu_page.html', context)
