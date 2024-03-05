#!/usr/bin/python3

# Author: Pedro Torres

import os
import datetime
import random
import subprocess
import string

def decimal_to_base(decimal, base):
    digs = string.digits + string.ascii_uppercase
    digits = []

    while decimal:
        digits.append(digs[decimal % base])
        decimal = decimal // base
    digits.reverse()

    return ''.join(digits)

def generate_test ( filenum, sourceBase, destBase, n, path="./" ):

    decimal = random.randint((10**(n-1)), ((10**n)-1))
    source = decimal_to_base(decimal, sourceBase);
    dest = decimal_to_base(decimal, destBase);

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write("{}\n{}\n{}\n{}".format(len(source), sourceBase, destBase, source))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write("{}".format(dest));

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 2, 10, 1, path="./" ) 
    generate_test ( 1, 10, 2, 2, path="./" ) 
    generate_test ( 2, 8, 16, 3, path="./" ) 
    generate_test ( 3, 16, 10, 4, path="./" ) 
    generate_test ( 4, 4, 36, 5, path="./" ) 
    generate_test ( 5, 8, 18, 6, path="./" ) 
    generate_test ( 6, 2, 36, 19, path="./" ) 


def test_anyToAny ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerString = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./anyToAny", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        resultString = result.stdout
        resultString.replace('\x00','')
        if verbose:
            print (' '.join(result.args))
            # print ("answerString")
            # print (answerString)
            # print ("resultString")
            # print (resultString)

        assert resultString == answerString, "Your answer doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./anyToAny returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False


def grade_anyToAny( path="./", verbose=False ):
    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile anyToAny.c.")
        return score

    if test_anyToAny(0, path, verbose):
        score += 2
        if test_anyToAny(1, path, verbose):
            score += 2
            if test_anyToAny(2, path, verbose):
                score += 2
                if test_anyToAny(3, path, verbose):
                    score += 2
                    if test_anyToAny(4, path, verbose):
                        score += 2
                        if test_anyToAny(5, path, verbose):
                            score += 2
                            if test_anyToAny(6, path, verbose):
                                score += 2
                                allPass = True
                                for filenum in range(7,18):
                                    generate_test (
                                        filenum,
                                        sourceBase=random.randrange(2,37),
                                        destBase=random.randrange(2,37),
                                        n=random.randrange(1,20),
                                        path=path
                                    )
                                    allPass &= test_anyToAny(filenum,path,verbose)
                                    if allPass:
                                        score += 1
                                    else:
                                        break

    print ("Score on anyToAny: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_anyToAny(verbose=True)
    exit()
