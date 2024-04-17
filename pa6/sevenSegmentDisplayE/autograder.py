#!/usr/bin/python3

import os
import datetime
import random
import subprocess
import string

# For a seven-segment display
# Dict of lists of decimal numerals for which each segment lights
numsForSegs = {
    'a':[0,2,3,5,6,7,8,9],
    'b':[0,1,2,3,4,7,8,9],
    'c':[0,1,3,4,5,6,7,8,9],
    'd':[0,2,3,5,6,8,9],
    'e':[0,2,6,8],
    'f':[0,4,5,6,8,9],
    'g':[2,3,4,5,6,8,9]
}

def generate_test ( filenum, segments=['e'], numeral=0, path="./" ):

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        infile.write("{}".format(numeral))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        for segment in segments:
            isLit = 1 if numeral in numsForSegs[segment] else 0
            outfile.write(segment + " = {}\n".format(isLit) )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, segments=['e'], numeral=0, path="./" )
    generate_test ( 1, segments=['e'], numeral=1, path="./" )
    generate_test ( 2, segments=['e'], numeral=2, path="./" )
    generate_test ( 3, segments=['e'], numeral=3, path="./" )
    generate_test ( 4, segments=['e'], numeral=4, path="./" )
    generate_test ( 5, segments=['e'], numeral=5, path="./" )
    generate_test ( 6, segments=['e'], numeral=6, path="./" )
    generate_test ( 7, segments=['e'], numeral=7, path="./" )
    generate_test ( 8, segments=['e'], numeral=8, path="./" )
    generate_test ( 9, segments=['e'], numeral=9, path="./" )

def test_sevenSegmentDisplayE ( filenum, path="./", verbose=False ):

    try:
        with open("{}tests/test{}.txt".format(path,filenum), "r") as infile:
            numeral = infile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("tests/test{}.txt missing".format(filenum))

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerDict = {}
            for line in outfile.read().split("\n"):
                if line != "":
                    words = line.split(" ")
                    if words[0] not in ["Read"]:
                        var = words[0]
                        val = words[2]
                        answerDict[var] = val
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["../circuitSimulator", "sevenSegmentDisplayE.v", numeral],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        resultDict = {}
        for line in result.stdout.split("\n"):
            if line != "":
                words = line.split(" ")
                if words[0] not in ["Read"]:
                    var = words[0]
                    val = words[2]
                    resultDict[var] = val

        if verbose:
            print (' '.join(result.args))
            print ("answer")
            print (answerDict)
            print ("result")
            print (result.stdout)
        assert resultDict == answerDict, "The circuit simulation result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ../circuitSimulator returned non-zero exit status.")
    # except ValueError as e:
    #     print (result.stdout)
    #     print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_sevenSegmentDisplayE( path="./", verbose=False ):

    score = 0

    if test_sevenSegmentDisplayE(0,path,verbose):
        score += 2.5
        if test_sevenSegmentDisplayE(1,path,verbose):
            score += 2.5
            if test_sevenSegmentDisplayE(2,path,verbose):
                score += 2.5
                if test_sevenSegmentDisplayE(3,path,verbose):
                    score += 2.5
                    if test_sevenSegmentDisplayE(4,path,verbose):
                        score += 2.5
                        if test_sevenSegmentDisplayE(5,path,verbose):
                            score += 2.5
                            if test_sevenSegmentDisplayE(6,path,verbose):
                                score += 2.5
                                if test_sevenSegmentDisplayE(7,path,verbose):
                                    score += 2.5
                                    if test_sevenSegmentDisplayE(8,path,verbose):
                                        score += 2.5
                                        if test_sevenSegmentDisplayE(9,path,verbose):
                                            score += 2.5

    print ("Score on sevenSegmentDisplayE: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_sevenSegmentDisplayE(verbose=True)
    exit()
