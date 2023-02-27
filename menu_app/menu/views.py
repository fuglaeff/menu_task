from collections import defaultdict

from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.db.models import Q

from .models import Menu, Folder


class IndexPageView(View):

    def get(self, request):
        all_menus = Menu.objects.all()

        return render(request, 'list_menus.html', {'menus': all_menus})


class FoldersPageView(View):

    @staticmethod
    def clean_path_nodes(path):
        path_nodes = {}
        for i in range(1, len(path)):
            if path[i] in path_nodes:
                raise Http404
            path_nodes[path[i]] = path[i-1]

        return path_nodes

    def get(self, request, menu_slug):
        path_string = request.GET.get('path')
        path = ['root', ]
        path_nodes = {}
        parent_query = Q(parent=None)
        if path_string:
            parents_slugs = path_string.strip('/').split('/')
            path += parents_slugs
            path_nodes = self.clean_path_nodes(path)
            parent_query = parent_query | Q(parent__slug__in=parents_slugs)

        folders = Folder.objects.filter(
            Q(menu__slug=menu_slug) & parent_query).select_related('parent')

        folders_nodes = defaultdict(list)
        for folder in folders:
            folder_parent = path[0]
            if folder.parent:
                folder_parent = folder.parent.slug
            if path_nodes.get(folder.slug, folder_parent) != folder_parent:
                raise Http404
            folders_nodes[folder_parent].append(folder)

        context = {
            'path': path,
            'folder_nodes': folders_nodes,
            'menu_slug': menu_slug,
        }

        return render(request, 'menu_page.html', context)
