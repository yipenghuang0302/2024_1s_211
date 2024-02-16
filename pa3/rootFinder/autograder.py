#!/usr/bin/python3

import random
import os
import datetime
import subprocess

def generate_test ( filenum, bound=4.0, power=2, precision=0.01, path="./" ):

    number = random.uniform(0,bound)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write( "{}\n".format(number) )
        infile.write( "{}\n".format(power) )
        infile.write( "{}\n".format(precision) )

    root = number**(1/power)
    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write( "{}\n".format(root) )
        outfile.write( "{}\n".format(precision) )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 2.0, 2, 0.01 )
    generate_test ( 1, 4.0, 3, 0.001 )
    generate_test ( 2, 8.0, 4, 0.0001 )
    generate_test ( 3, 16.0, 5, 0.00001 )

def test_rootFinder ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = outfile.readline()
            precision = outfile.readline()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ['./rootFinder', "tests/test{}.txt".format(filenum)],
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
            print ("\n")
        assert abs(float(answer)-float(result.stdout))<float(precision), "The printed result is not within the desired precision of answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        # print (e.output)
        print ("Calling ./rootFinder returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting; it should be formatted as a floating point number.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_rootFinder( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile rootFinder.")
        return score

    if test_rootFinder(0,path,verbose):
        score += 1
        if test_rootFinder(1,path,verbose):
            score += 1
            if test_rootFinder(2,path,verbose):
                score += 1
                if test_rootFinder(3,path,verbose):
                    score += 1
                    for filenum in range(4,25):
                        generate_test (
                            filenum=filenum,
                            bound=32.0,
                            power=random.randrange(1,8),
                            precision=0.000001,
                            path=path
                        )
                        if test_rootFinder(filenum,path,verbose):
                            score += 1

    print ("Score on rootFinder: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_rootFinder(verbose=True)
    exit()
