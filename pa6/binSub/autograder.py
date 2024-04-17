#!/usr/bin/python3

import os
import datetime
import random
import subprocess
import string

def generate_test ( filenum, minuend=0, subtrahend=0, path="./" ):

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        infile.write("{}\n".format(minuend))
        infile.write("{}\n".format(subtrahend))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write("difference" + " = {}\n".format((minuend-subtrahend)%256) )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, minuend=0, subtrahend=0, path="./" )
    generate_test ( 1, minuend=1, subtrahend=0, path="./" )
    generate_test ( 2, minuend=2, subtrahend=1, path="./" )
    generate_test ( 3, minuend=0, subtrahend=1, path="./" )
    generate_test ( 4, minuend=1, subtrahend=2, path="./" )
    generate_test ( 5, minuend=2, subtrahend=2, path="./" )

def test_binSub ( filenum, path="./", verbose=False ):

    try:
        with open("{}tests/test{}.txt".format(path,filenum), "r") as infile:
            minuend = infile.readline().strip()
            subtrahend = infile.readline().strip()
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
            ["../circuitSimulator", "binSub.v", minuend, subtrahend],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        resultDict = {}
        for line in result.stdout.split("\n"):
            # print ("line = ", line)
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

def grade_binSub( path="./", verbose=False ):

    score = 0

    if test_binSub(0,path,verbose):
        score += 1
        if test_binSub(1,path,verbose):
            score += 1
            if test_binSub(2,path,verbose):
                score += 1
                if test_binSub(3,path,verbose):
                    score += 1
                    if test_binSub(4,path,verbose):
                        score += 1
                        if test_binSub(5,path,verbose):
                            score += 1
                            for filenum in range(6,25):
                                minuend = random.randrange(256)
                                subtrahend = random.randrange(256)
                                generate_test ( filenum, minuend=minuend, subtrahend=subtrahend, path=path )
                                if test_binSub(filenum,path,verbose):
                                    score += 1
                                else:
                                    break

    print ("Score on binSub: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_binSub(verbose=True)
    exit()
