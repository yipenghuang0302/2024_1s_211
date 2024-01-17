#!/usr/bin/python3

import os
import datetime
import random
import subprocess

def generate_test ( filenum, is_square, max=3, path="./" ):

    if is_square:
        root = random.randrange(max)
        square = root * root
    else:
        accidentally_is_square = True
        while accidentally_is_square:
            square = random.randrange(max)
            root = int ( pow(square,1/2) )
            # print("square")
            # print(square)
            # print("pow(square,1/2)")
            # print(pow(square,1/2))
            # print("root")
            # print(root)
            accidentally_is_square = root*root == square

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write(str(square))


    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        if is_square:
            outfile.write(str(root))
        else:
            outfile.write("square root not integer")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, True, max=2, path="./" )
    generate_test ( 1, True, max=4, path="./" )
    generate_test ( 2, True, max=8, path="./" )
    generate_test ( 3, False, max=16, path="./" )
    generate_test ( 4, False, max=32, path="./" )
    generate_test ( 5, False, max=64, path="./" )
    generate_test ( 6, True, max=128, path="./" )
    generate_test ( 7, False, max=256, path="./" )

def test_rootFinder ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerString = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./rootFinder", "tests/test{}.txt".format(filenum)],
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
        assert resultString == answerString, "The program output is not the square root, or program failed to reply \"square root not integer\".".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./rootFinder returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_rootFinder( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile rootFinder.c.")
        return score

    if test_rootFinder(0,path,verbose):
        score += 1
        if test_rootFinder(1,path,verbose):
            score += 1
            if test_rootFinder(2,path,verbose):
                score += 1
                if test_rootFinder(3,path,verbose):
                    score += 1
                    if test_rootFinder(4,path,verbose):
                        score += 1
                        if test_rootFinder(5,path,verbose):
                            score += 1
                            if test_rootFinder(6,path,verbose):
                                score += 1
                                if test_rootFinder(7,path,verbose):
                                    score += 1
                                    allPass = True
                                    for filenum in range(8,15):
                                        generate_test (
                                            filenum,
                                            is_square=bool(random.getrandbits(1)),
                                            max=128,
                                            path=path
                                        )
                                        allPass &= test_rootFinder(filenum,path,verbose)
                                        if allPass:
                                            score += 1
                                        else:
                                            break

    print ("Score on rootFinder: {} out of 15.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_rootFinder(verbose=True)
    exit()
