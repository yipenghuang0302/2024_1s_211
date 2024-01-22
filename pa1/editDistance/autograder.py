#!/usr/bin/python3

import os
import datetime
import random
import subprocess
import sys
from Levenshtein import distance

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def generate_test ( filenum, min_word_length=4, max_distance=1, path="./" ):

    word_file = "/usr/share/dict/words"
    words = open(word_file).read().splitlines()

    calculated_distance = sys.maxsize
    while max_distance<calculated_distance:
        word0 = ""
        word1 = ""
        while not is_ascii(word0) or len(word0)<min_word_length:
            word0 = random.choice(words)
        while not is_ascii(word1) or len(word1)<min_word_length:
            word1 = random.choice(words)
        calculated_distance = distance(word0, word1)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write(word0)
        infile.write("\n")
        infile.write(word1)

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write(f"{calculated_distance}")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, min_word_length=2, max_distance=1, path="./" )
    generate_test ( 1, min_word_length=4, max_distance=2, path="./" )
    generate_test ( 2, min_word_length=6, max_distance=3, path="./" )
    generate_test ( 3, min_word_length=8, max_distance=4, path="./" )
    generate_test ( 4, min_word_length=10, max_distance=5, path="./" )
    generate_test ( 5, min_word_length=12, max_distance=6, path="./" )
    generate_test ( 6, min_word_length=14, max_distance=7, path="./" )
    generate_test ( 7, min_word_length=16, max_distance=8, path="./" )

def test_editDistance ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerString = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./editDistance", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=3).total_seconds(),
        )

        resultString = result.stdout.strip()

        if verbose:
            print (' '.join(result.args))
            # print ("answer")
            # print (answerString)
            # print ("result")
            # print (result.stdout)
        assert resultString == answerString, "The program output does not output the correct Levenshtein distance.".format(filenum)
        return True
    except subprocess.TimeoutExpired as e:
        print (e.output)
        print ("Calling ./editDistance with the previous test case timed out. A more efficient algorithm implementation is needed.")
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./editDistance returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_editDistance( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile editDistance.c.")
        return score

    if test_editDistance(0,path,verbose):
        score += 1
        if test_editDistance(1,path,verbose):
            score += 1
            if test_editDistance(2,path,verbose):
                score += 1
                if test_editDistance(3,path,verbose):
                    score += 1
                    if test_editDistance(4,path,verbose):
                        score += 1
                        if test_editDistance(5,path,verbose):
                            score += 2
                            if test_editDistance(6,path,verbose):
                                score += 2
                                if test_editDistance(7,path,verbose):
                                    score += 2
                                    allPass = True
                                    for filenum in range(8,15):
                                        generate_test (
                                            filenum,
                                            min_word_length=16,
                                            max_distance=12,
                                            path=path
                                        )
                                        allPass &= test_editDistance(filenum,path,verbose)
                                        if allPass:
                                            score += 2
                                        else:
                                            break

    print ("Score on editDistance: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_editDistance(verbose=True)
    exit()
