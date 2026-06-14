import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django import forms
from .models import Project, Skill
from users.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        widgets = {
            'status': forms.Select(choices=Project.STATUS_CHOICES),
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url:
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url


def project_list_view(request):
    projects_list = Project.objects.filter(status='open').order_by('-created_at')
    skill_filter = request.GET.get('skill')
    active_skill = None
    
    if skill_filter:
        try:
            active_skill = Skill.objects.get(name=skill_filter)
            projects_list = projects_list.filter(skills=active_skill)
        except Skill.DoesNotExist:
            pass
    
    paginator = Paginator(projects_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_skills = Skill.objects.all().order_by('name')
    
    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'all_skills': all_skills,
        'active_skill': active_skill.name if active_skill else None,
    })


def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({'error': 'Нет прав'}, status=403)
    if project.status == 'open':
        project.status = 'closed'
        project.save()
    return JsonResponse({'status': 'ok', 'project_status': project.status})


@login_required
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        is_participant = False
    else:
        project.participants.add(request.user)
        is_participant = True
    return JsonResponse({'status': 'ok', 'is_participant': is_participant})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect(f'/projects/{project.id}/')
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return redirect(f'/projects/{project_id}/')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(f'/projects/{project_id}/')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True, 'project': project})


def skill_autocomplete(request):
    q = request.GET.get('q', '')
    skills = Skill.objects.filter(name__istartswith=q).order_by('name')[:10]
    data = [{'id': s.id, 'name': s.name} for s in skills]
    return JsonResponse(data, safe=False)


@login_required
def add_project_skill(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({'error': 'Нет прав'}, status=403)
    
    data = json.loads(request.body)
    skill_id = data.get('skill_id')
    skill_name = data.get('name')
    created = False
    added = False
    
    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    else:
        skill, created = Skill.objects.get_or_create(name=skill_name)
    
    if skill not in project.skills.all():
        project.skills.add(skill)
        added = True
    
    return JsonResponse({
        'skill_id': skill.id,
        'created': created,
        'added': added,
    })


@login_required
def remove_project_skill(request, project_id, skill_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse({'error': 'Нет прав'}, status=403)
    
    skill = get_object_or_404(Skill, id=skill_id)
    
    if skill in project.skills.all():
        project.skills.remove(skill)
    
    return JsonResponse({'status': 'ok'})