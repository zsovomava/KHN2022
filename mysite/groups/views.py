from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Event, Group, UserGroup
from .permissions import IsOwnerOrReadOnly


class GroupListView(ListView):
    model = Group
    ordering = ['name']
    paginate_by = 8

    def get_queryset(self):
        queryset = Group.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q))
        return queryset


class GroupDetailView(DetailView):
    model = Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_member'] = self.request.user.is_authenticated and self.object.user_is_member(
            self.request.user)
        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        group = self.get_object()
        return self.request.user == group.owner


class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group

    def get_success_url(self):
        return reverse('groups:group-list')

    def test_func(self):
        group = self.get_object()
        return self.request.user == group.owner or self.request.user.is_staff and not group.author.is_superuser


@login_required
def group_leave(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.user != group.owner:
        conn = group.get_member(request.user)
        if conn:
            conn.delete()
            messages.success(request, 'Sikeresen elhagyta a csoportot.')
    return redirect('groups:group-list')


@login_required
def group_join(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.user != group.owner:
        conn = group.get_member(request.user)
        if not conn:
            conn = UserGroup(user=request.user, group=group)
            conn.save()
            messages.success(request, 'Sikeresen csatlakozott a csoporthoz.')
    return redirect('groups:group-detail', pk=group.id)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Event.objects.all()
        if self.action == 'list':
            group = self.request.query_params.get('group')
            if group:
                queryset = queryset.filter(group__id=group)
            start = self.request.query_params.get('start')
            if start:
                queryset = queryset.filter(end__gte=
                    datetime.utcfromtimestamp(int(start) // 1e3))
            end = self.request.query_params.get('end')
            if end:
                queryset = queryset.filter(start__lte=
                    datetime.utcfromtimestamp(int(end) // 1e3))
        return queryset

    def get_serializer_class(self):
        group_choices = [x.group for x in self.request.user.usergroups.all(
        )] if self.request.user.is_authenticated else []

        class EventSerializer(serializers.ModelSerializer):
            group = serializers.ChoiceField(group_choices, write_only=True)
            owner_name = serializers.ReadOnlyField(
                source='owner.username')

            class Meta:
                model = Event
                fields = ['id', 'title', 'group',
                          'owner_name', 'start', 'end']

        return EventSerializer
