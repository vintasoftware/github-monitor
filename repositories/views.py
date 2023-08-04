from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Commit, Repository
from .serializers import CommitSerializer, RepositorySerializer
from common.services import GitHubService
from repositories.tasks import capture_repository_commits_task


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def commit_list_view(request):
    commits = Commit.objects.all()
    serializer = CommitSerializer(commits, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def repository_create_view(request):
    serializer = RepositorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    github_client = GitHubService()
    repository = serializer.validated_data['name']

    if not github_client.repository_exists(request.user, repository):
        return Response("Repository does not exist in your Github Account.", status=status.HTTP_404_NOT_FOUND)

    if Repository.objects.filter(name=repository).exists():
        return Response("Repository is already added to Github monitor", status=status.HTTP_409_CONFLICT)

    # add background job to save repo commits here
    # github_client.get_repository_commits(request.user, repository)
    capture_repository_commits_task.delay(str(request.user), repository)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)
