from ..models import Project

def get_projects():
    return Project.objects.all()

def create_project(form):
    project = form.save()
    return project
