#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the countingValleys function below.
def countingValleys(n, s):
    current_elevation = 0
    valley_count = 0
    for i in range(len(s)):
        if current_elevation == 0 and (s[i-1] == "U"):
            valley_count += 1
        if s[i] == "U":
            current_elevation += 1
        if s[i] == "D":
            current_elevation += -1
        print(current_elevation)
    return valley_count


if __name__ == '__main__':
    print(countingValleys(8, "UDDDUDUU"))
