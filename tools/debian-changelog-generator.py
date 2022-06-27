#!/usr/bin/python3
from datetime import datetime
from datetime import timezone 
import subprocess
import re
import argparse

def GetTagDate(GitTag):
    DebianFormat=r"%a, %d %b %Y %H:%M:%S %z"
    if GitTag != "0.0.0":
        GitLogDate=subprocess.run(["git","show","--format=%aI","-s",f"{GitTag}^{{commit}}"],capture_output=True,universal_newlines=True,check=True)
        LogDate=GitLogDate.stdout.strip()
        LogDateIso=datetime.fromisoformat(LogDate)
        return LogDateIso.strftime(DebianFormat)
    else:
        LogDate=datetime.now(timezone.utc)
        return LogDate.strftime(DebianFormat)

ChangeStart=re.compile(r"^<!-- changelog start -->$")
ChangeEnd=re.compile(r"^<!-- changelog end -->$")
ChangeTag=re.compile(r"^## <!-- release tag -->\[([0-9]+\.[0-9]+\.[0-9]+)\]")
ChangeLine=re.compile(r"^- (.*)<!-- change line -->$")
ProcessLine=False
GitTag=None
## <!-- release tag -->
DevChangeLog=f"""otpgui (0.0.0-1) UNRELEASED; urgency=medium

  * Development version

 -- Gianluca mascolo <gianluca@gurutech.it>  {GetTagDate('0.0.0')}"""

parser = argparse.ArgumentParser()
parser.add_argument("-c","--changelog", help="Path to CHANGELOG.md", type=str,default="CHANGELOG.md")
parser.add_argument("-d","--dev", help="Development Changelog",action="store_true")
args = parser.parse_args()

if args.dev:
    print(f"{DevChangeLog}")
else:
    with open(args.changelog) as cl:
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
