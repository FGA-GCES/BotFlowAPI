from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404

from api.models import Project, Story, Intent
from api.parser import StoryParser, IntentParser, DomainParser


class StoriesFile(APIView):
    """
    Receives a get request with a project id and returns
    a json response with the markdown string, containing
    all stories of the project, in the body.
    """

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        stories = Story.objects.filter(project=project)
        
        if not stories:
            raise Http404
        
        parser = StoryParser()
        markdown_str = ''

        for story in stories:
            markdown_str += parser.parse(story)
        
        return JsonResponse({'content': markdown_str})  


class IntentsFile(APIView):
    """
    Receives a get request with a project id and returns
    a json response with the markdown string, containing
    all intents of the project, in the body.
    """

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        stories = Story.objects.filter(project=project)
        intents = Intent.objects.filter(project=project)

        stories_intents = []
        for s in stories:
            for c in s.content:
                c = dict(c)
                if c['type'] == 'intent':
                    stories_intents.append(c['name'])

        used_intents = filter(lambda intent: intent.name in stories_intents, intents)

        if not intents:
            raise Http404

        parser = IntentParser()
        markdown_str = ''

        for intent in used_intents:
            markdown_str += parser.parse(intent)

        return JsonResponse({'content': markdown_str})


class DomainFile(APIView):
    """
    Receives a get request with a project id and returns
    a json response with markdown string, containing all
    domain content, in the body.
    """

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        parser = DomainParser()
        markdown_str = parser.parse(project)

        return JsonResponse({'content': markdown_str})
