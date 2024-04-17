#!/usr/bin/python3

import os
import datetime
import random
import subprocess
import string

def generate_test ( filenum, number=0, path="./" ):

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write("{}".format(number))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write('b' + " = {}\n".format(-number%256) )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, number=1, path="./" )
    generate_test ( 1, number=0, path="./" )
    generate_test ( 2, number=2, path="./" )
    generate_test ( 3, number=127, path="./" )
    generate_test ( 4, number=128, path="./" )
    generate_test ( 5, number=129, path="./" )

def test_negator ( filenum, path="./", verbose=False ):

    try:
        with open("{}tests/test{}.txt".format(path,filenum), "r") as infile:
            number = infile.read()
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
            ["../circuitSimulator", "negator.v", number],
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

def grade_negator( path="./", verbose=False ):

    score = 0

    if test_negator(0,path,verbose):
        score += 1
        if test_negator(1,path,verbose):
            score += 1
            if test_negator(2,path,verbose):
                score += 1
                if test_negator(3,path,verbose):
                    score += 1
                    if test_negator(4,path,verbose):
                        score += 1
                        if test_negator(5,path,verbose):
                            score += 1
                            for filenum in range(6,25):
                                number = random.randrange(256)
                                generate_test ( filenum, number=number, path=path )
                                if test_negator(filenum,path,verbose):
                                    score += 1
                                else:
                                    break

    print ("Score on negator: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_negator(verbose=True)
    exit()
