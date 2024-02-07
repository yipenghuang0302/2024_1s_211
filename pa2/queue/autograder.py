#!/usr/bin/python3

import os
import datetime
import random
import subprocess

def generate_test ( filenum, length, path="./" ):

    queue = []

    # print (string)
    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        for _ in range(length):
            enqueue = bool(random.getrandbits(1))
            if enqueue:
                num = random.randrange(256)
                queue.append(num)
                infile.write("ENQUEUE {}\n".format(num))
            elif queue:
                infile.write("DEQUEUE\n".format(num))
                queue.pop(0)

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        for num in queue:
            outfile.write("{}\n".format(num))

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 4, path="./"  )
    generate_test ( 1, 16, path="./"  )
    generate_test ( 2, 256, path="./"  )
    generate_test ( 3, 65536, path="./"  )

def test_queue ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerlist = [ int(num) for num in outfile.read().split() ]
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./queue", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        resultlist = [int(string) for string in result.stdout.split()]

        if verbose:
            print (' '.join(result.args))
            # print ("answerlist")
            # print (answerlist)
            # print ("resultlist")
            # print (resultlist)
        assert resultlist == answerlist, "Your answer doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./queue returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_queue( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile queue.c.")
        return score

    if test_queue(0,path,verbose):
        score += 5
        if test_queue(1,path,verbose):
            score += 5
            if test_queue(2,path,verbose):
                score += 5
                if test_queue(3,path,verbose):
                    score += 5

                    allpass = True
                    for filenum in range(4,12):
                        generate_test ( filenum=filenum, length=65536, path=path )
                        allpass &= test_queue(filenum,path,verbose)
                    if allpass:
                        score += 5

    print ("Score on queue: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_queue(verbose=True)
    exit()
