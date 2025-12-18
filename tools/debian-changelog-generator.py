#!/usr/bin/python3
import argparse
import os
import re
import subprocess
from datetime import datetime, timezone

import requests


class TagNotFoundError(Exception):
    """Raised when a git tag is not found on GitHub."""

    pass


def GetTagDate(GitTag, GitMethod):
    DebianFormat = r"%a, %d %b %Y %H:%M:%S %z"
    if GitTag != "0.0.0":
        if GitMethod == "cli":
            GitLogDate = subprocess.run(["git", "show", "--format=%aI", "-s", f"{GitTag}^{{commit}}"], capture_output=True, universal_newlines=True, check=True)
            LogDate = GitLogDate.stdout.strip()
        elif GitMethod == "api":
            GithubToken = os.environ["GITHUB_TOKEN"]
            h = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GithubToken}"}
            r = requests.get(f"https://api.github.com/repos/gianluca-mascolo/otpgui/git/refs/tags/{GitTag}", headers=h)
            if r.status_code == 404:
                raise TagNotFoundError(f"Tag '{GitTag}' not found on GitHub. Please ensure the tag exists or remove it from CHANGELOG.md")
            if r.status_code != 200:
                raise TagNotFoundError(f"GitHub API error for tag '{GitTag}': HTTP {r.status_code} - {r.text}")
            response_json = r.json()
            if "object" not in response_json:
                raise TagNotFoundError(f"Invalid GitHub API response for tag '{GitTag}': missing 'object' field. Response: {response_json}")
            ObjectUrl = response_json["object"]["url"]
            r = requests.get(ObjectUrl, headers=h)
            TagInfo = r.json().get("author")
            if TagInfo is None:
                TagInfo = r.json().get("tagger")
            LogDate = re.sub("Z$", "+00:00", TagInfo["date"])
        LogDateIso = datetime.fromisoformat(LogDate)
        return LogDateIso.strftime(DebianFormat)
    else:
        LogDate = datetime.now(timezone.utc)
        return LogDate.strftime(DebianFormat)


ChangeStart = re.compile(r"^<!-- changelog start -->$")
ChangeEnd = re.compile(r"^<!-- changelog end -->$")
ChangeTag = re.compile(r"^## <!-- release tag -->\[([0-9]+\.[0-9]+\.[0-9]+)\]")
ChangeLine = re.compile(r"^- (.*)<!-- change line -->$")
ProcessLine = False
GitTag = None
DevChangeLog = f"""otpgui (0.0.0-1) UNRELEASED; urgency=medium

  * Development version

 -- Gianluca Mascolo <gianluca@gurutech.it>  {GetTagDate('0.0.0', 'cli')}"""

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--changelog", help="Path to CHANGELOG.md", type=str, default="CHANGELOG.md")
parser.add_argument("-m", "--method", help="Method to retrieve git tags", choices=["cli", "api"], type=str, default="cli")
parser.add_argument("-d", "--dev", help="Development Changelog", action="store_true")
args = parser.parse_args()

if args.dev:
    print(f"{DevChangeLog}")
else:
    with open(args.changelog) as cl:
        lines = cl.readlines()
        for line in lines:
            if ChangeStart.match(line):
                ProcessLine = True
            if ChangeEnd.match(line):
                ProcessLine = False
                print(f"\n -- Gianluca Mascolo <gianluca@gurutech.it>  {GetTagDate(GitTag, args.method)}")
            if ProcessLine:
                if ChangeTag.match(line):
                    if GitTag:
                        print(f"\n -- Gianluca Mascolo <gianluca@gurutech.it>  {GetTagDate(GitTag, args.method)}\n")
                    GitTagSearch = ChangeTag.search(line)
                    GitTag = GitTagSearch.group(1)
                    print(f"otpgui ({GitTag}-1) unstable; urgency=medium\n")
                if ChangeLine.match(line):
                    LogLineSearch = ChangeLine.search(line)
                    LogLine = LogLineSearch.group(1)
                    print(f"  * {LogLine}")
