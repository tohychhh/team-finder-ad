import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from projects.forms import ProjectForm
from projects.models import Project, Skill
from projects.service import paginate_queryset
from team_finder.constants import (
    PAGINATION_PAGE_SIZE,
    SKILL_AUTOCOMPLETE_LIMIT,
    STATUS_CLOSED,
    STATUS_OPEN,
)


def project_list_view(request):
    projects_list = Project.objects.filter(
        status=STATUS_OPEN
    ).select_related('owner').prefetch_related('participants', 'skills').order_by('-created_at')

    skill_filter = request.GET.get('skill')
    active_skill = None

    if skill_filter:
        try:
            active_skill = Skill.objects.get(name=skill_filter)
            projects_list = projects_list.filter(skills=active_skill)
        except Skill.DoesNotExist:
            pass

    page_obj = paginate_queryset(projects_list, request)
    all_skills = Skill.objects.all().order_by('name')

    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'all_skills': all_skills,
        'active_skill': active_skill.name if active_skill else None,
    })


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants', 'skills'),
        id=project_id
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
@require_http_methods(["POST"])
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({'error': 'Нет прав'}, status=HTTPStatus.FORBIDDEN)

    if project.status == STATUS_OPEN:
        project.status = STATUS_CLOSED
        project.save()

    return JsonResponse({'status': 'ok', 'project_status': project.status})


@login_required
@require_http_methods(["POST"])
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    is_participant = project.participants.filter(id=request.user.id).exists()

    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({'status': 'ok', 'is_participant': not is_participant})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:project_detail', project.id)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return redirect('projects:project_detail', project_id)

    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:project_detail', project_id)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True, 'project': project})


def skill_autocomplete(request):
    q = request.GET.get('q', '')
    skills = Skill.objects.filter(name__istartswith=q).order_by('name')[:SKILL_AUTOCOMPLETE_LIMIT]
    data = [{'id': s.id, 'name': s.name} for s in skills]
    return JsonResponse(data, safe=False)


@login_required
@require_http_methods(["POST"])
def add_project_skill(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({'error': 'Нет прав'}, status=HTTPStatus.FORBIDDEN)

    data = json.loads(request.body)
    skill_id = data.get('skill_id')
    skill_name = data.get('name')
    created = False
    added = False

    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    else:
        skill, created = Skill.objects.get_or_create(name=skill_name)

    if not project.skills.filter(id=skill.id).exists():
        project.skills.add(skill)
        added = True

    return JsonResponse({
        'skill_id': skill.id,
        'created': created,
        'added': added,
    })


@login_required
@require_http_methods(["POST"])
def remove_project_skill(request, project_id, skill_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({'error': 'Нет прав'}, status=HTTPStatus.FORBIDDEN)

    skill = get_object_or_404(Skill, id=skill_id)

    if project.skills.filter(id=skill.id).exists():
        project.skills.remove(skill)

    return JsonResponse({'status': 'ok'})


@login_required
def favorites_view(request):
    user = request.user
    favorite_projects = user.favorites.all()
    page_obj = paginate_queryset(favorite_projects, request, PAGINATION_PAGE_SIZE)
    return render(request, 'projects/favorite_projects.html', {'projects': page_obj})
