import requests
import json
from repositories.serializers import CommitSerializer
from repositories.models import Repository, Commit
from social_django.models import UserSocialAuth
import datetime


class GitHubService:
    def __init__(self):
        self.BASE_URL = 'https://api.github.com'
        self.ACCESS_TOKEN = None

    def get_request_headers(self, user):
        if self.ACCESS_TOKEN is None:
            self.set_access_token(user)

        return {
            'Authorization': f'token {self.ACCESS_TOKEN}'
        }

    def set_access_token(self, user):
        social_user_data = UserSocialAuth.objects.get(user__username=user)
        self.ACCESS_TOKEN = social_user_data.extra_data["access_token"]

    def repository_exists(self, user, repository):
        get_repository_response = requests.get(
            f"{self.BASE_URL}/repos/{user}/{repository}", headers=self.get_request_headers(user))

        return get_repository_response.status_code == 200

    def get_repository_commits(self, user, repository):
        page = 1
        all_commits = []
        has_next = True

        while has_next:
            commits_response = requests.get(
                f"{self.BASE_URL}/repos/{user}/{repository}/commits?page={page}", headers=self.get_request_headers(user))
            commits_response_data = json.loads(commits_response.text)

            if (len(commits_response_data)):
                [all_commits.append(commit)
                 for commit in commits_response_data]
                page = page + 1
                commits_response_data = []
            else:
                break

        return all_commits
