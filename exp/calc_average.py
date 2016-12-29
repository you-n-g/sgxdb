#!/usr/bin/env python

import sys
import re

times =  []
for line in sys.stdin.readlines():
    times.extend(re.findall(r".*0:0(\d+\.\d+)elapsed.*", line))
print times
print "first 5 elements are truncated!!"
times = times[5:]

print sum([float(t) for t in times]) / len(times)
