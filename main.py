#!/usr/bin/env python3

import os
import sys
import yaml
import datetime as dt

from github import Github, Auth
from cron_validator import CronValidator

GITHUB_TOKEN=sys.argv[1]
REPO_ID = int(os.environ.get("GITHUB_REPOSITORY_ID", "-1"))
REPO_OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "Null")

auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)
repo = gh.get_repo(REPO_ID)

with open("recurring_tasks.yml") as f:
    tasks = yaml.safe_load(f)

now = dt.datetime.utcnow()

for task in tasks:
    if CronValidator.match_datetime(task['schedule'], now):
        repo.create_issue(
            title=task['title'],
            body=task['description'],
            labels=task['labels'],
            assignee=REPO_OWNER
        )
