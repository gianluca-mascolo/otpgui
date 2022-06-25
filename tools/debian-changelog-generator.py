#!/usr/bin/python3
from datetime import datetime
import subprocess
import re

def GetTagDate(GitTag):
    GitLogDate=subprocess.run(["git","show","--format=%aI","-s",f"{GitTag}^{{commit}}"],capture_output=True,universal_newlines=True,check=True)
    LogDate=GitLogDate.stdout.strip()
    LogDateIso=datetime.fromisoformat(LogDate)
    DebianFormat=r"%a, %d %b %Y %H:%M:%S %z"
    #print(f"D: {LogDateIso.strftime(debfmt) }")
    return LogDateIso.strftime(DebianFormat)

ChangeStart=re.compile(r"^<!-- changelog start -->$")
ChangeEnd=re.compile(r"^<!-- changelog end -->$")
ChangeTag=re.compile(r"^## <!-- release tag -->\[([0-9]+\.[0-9]+\.[0-9]+)\]")
ChangeLine=re.compile(r"^<!-- change line -->- (.*)$")
ProcessLine=False
GitTag=None
## <!-- release tag -->

with open("CHANGELOG.md") as cl:
    lines = cl.readlines()
    for line in lines:
        if ChangeStart.match(line):
            ProcessLine=True
        if ChangeEnd.match(line):
            ProcessLine=False
            print(f"\n -- Gianluca mascolo <gianluca@gurutech.it>  {GetTagDate(GitTag)}")
        if ProcessLine:
            if ChangeTag.match(line):
                if GitTag:
                    print(f"\n -- Gianluca mascolo <gianluca@gurutech.it>  {GetTagDate(GitTag)}\n")
                GitTagSearch = ChangeTag.search(line)
                GitTag=GitTagSearch.group(1)
                print(f"otpgui ({GitTag}-1) unstable; urgency=medium\n")
            if ChangeLine.match(line):
                LogLineSearch = ChangeLine.search(line)
                LogLine=LogLineSearch.group(1)
                print(f"  * {LogLine}")