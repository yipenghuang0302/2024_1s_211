#!/usr/bin/python3

import os
import datetime
import random
import subprocess
from math import sqrt


def is_prime ( p: int ):
    if p > 1:
        for i in range(2, int(p/2)+1):
            if (p % i) == 0:
                return False
        else:
            return True
    else:
        return False

def generate_test ( filenum, is_perfect, stop, path="./" ):

    p = stop

    if is_perfect:
        mersenne_found = False
        while not mersenne_found:
            m_p = 2**p - 1
            if is_prime ( m_p ):
                mersenne_found = True
            else:
                p = p-1
    else:
        mersenne_found = True
        while mersenne_found:
            m_p = 2**p - 1
            if not is_prime ( m_p ):
                mersenne_found = False
            else:
                p = p-1

    perfect_candidate = 2**(p-1) * m_p

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        infile.write(str(perfect_candidate))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        if is_perfect:
            outfile.write(str(m_p))
        else:
            outfile.write(str(-1))

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    # p m_p = 2**p - 1 perfect_candidate = 2**(p-1) * m_p
    # F 0 -1
    # F 1 1 1
    # T 2 3 6
    # T 3 7 28
    # F 4 15 120
    # T 5 31 496
    # F 6 63 2016
    # T 7 127 8128
    # F 8 255 32640
    # F 9 511 130816
    # 10
    # 11
    # 12
    # T 13 8191 33550336

    generate_test ( 0, True , stop=2, path="./" )
    generate_test ( 1, True , stop=3, path="./" )
    generate_test ( 2, False, stop=4, path="./" )
    generate_test ( 3, True , stop=5, path="./" )
    generate_test ( 4, False, stop=6, path="./" )
    generate_test ( 5, True , stop=7, path="./" )
    generate_test ( 6, False, stop=8, path="./" )
    generate_test ( 7, False, stop=9, path="./" )

def test_euclidEuler ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerString = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./euclidEuler", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        resultString = result.stdout.strip()

        if verbose:
            print (' '.join(result.args))
            # print ("answerString")
            # print (answerString)
            # print ("resultString")
            # print (resultString)
        assert resultString == answerString, "The program output does not print the corresponding prime number, or program failed to return -1 if input is not a perfect number.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./euclidEuler returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_euclidEuler( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile euclidEuler.c.")
        return score

    if test_euclidEuler(0,path,verbose):
        score += 1
        if test_euclidEuler(1,path,verbose):
            score += 1
            if test_euclidEuler(2,path,verbose):
                score += 1
                if test_euclidEuler(3,path,verbose):
                    score += 1
                    if test_euclidEuler(4,path,verbose):
                        score += 1
                        if test_euclidEuler(5,path,verbose):
                            score += 1
                            if test_euclidEuler(6,path,verbose):
                                score += 1
                                if test_euclidEuler(7,path,verbose):
                                    score += 1
                                    allPass = True
                                    for filenum in range(8,15):
                                        generate_test (
                                            filenum,
                                            is_perfect=bool(random.getrandbits(1)),
                                            stop=2*filenum,
                                            path=path
                                        )
                                        allPass &= test_euclidEuler(filenum,path,verbose)
                                        if allPass:
                                            score += 1
                                        else:
                                            break

    print ("Score on euclidEuler: {} out of 15.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_euclidEuler(verbose=True)
    exit()
