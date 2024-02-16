#!/usr/bin/python3

import random
import os
import datetime
import subprocess
import math

def generate_test ( filenum, precision=0.01, path="./" ):

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write( "{}\n".format(precision) )

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write( "{}\n".format(math.pi) )
        outfile.write( "{}\n".format(precision) )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 0.01 )
    generate_test ( 1, 0.001 )
    generate_test ( 2, 0.0001 )
    generate_test ( 3, 0.00001 )

def test_monteCarloPi ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = outfile.readline()
            precision = outfile.readline()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ['./monteCarloPi', "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )
        if verbose:
            print (' '.join(result.args))
            print ("answer")
            print (float(answer))
            print ("precision")
            print (float(precision))
            print ("result")
            print (float(result.stdout))
        assert abs(float(answer)-float(result.stdout))<float(precision), "The printed result is not within the desired precision of answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./monteCarloPi returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting; it should be formatted as a floating point number.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_monteCarloPi( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile monteCarloPi.")
        return score

    if test_monteCarloPi(0,path,verbose):
        score += 4
        if test_monteCarloPi(1,path,verbose):
            score += 4
            if test_monteCarloPi(2,path,verbose):
                score += 4
                if test_monteCarloPi(3,path,verbose):
                    score += 4

                    allpass = True
                    for filenum in range(4,16):
                        generate_test (
                            filenum=filenum,
                            precision=0.000001,
                            path=path
                        )
                        allpass &= test_monteCarloPi(filenum,path,verbose)
                    if allpass:
                        score += 9

    print ("Score on monteCarloPi: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_monteCarloPi(verbose=True)
    exit()
