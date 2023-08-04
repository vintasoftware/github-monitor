from repositories.models import Commit, Repository

from githubmonitor.celery import app
from celery import shared_task
from common.services import GitHubService


@shared_task()
def capture_repository_commits_task(user, repository):
    repository_object = Repository.objects.get(name=repository)
    github_client = GitHubService()
    commits = github_client.get_repository_commits(user, repository)
    # FIXME: this could be optimized as a bulk insert inside a db transaction
    for commit_raw_data in commits:
        Commit(
            message=commit_raw_data['commit']['message'],
            sha=commit_raw_data['sha'],
            author=commit_raw_data['commit']['author']['name'],
            url=commit_raw_data['url'],
            # avatar=commit_raw_data['commit']['author'].get('avatar_url', ''),
            date=commit_raw_data['commit']['author']['date'],
            repository=repository_object
        ).save()

    return {'repository': repository, 'captured_commits': [commit['sha'] for commit in commits]}
