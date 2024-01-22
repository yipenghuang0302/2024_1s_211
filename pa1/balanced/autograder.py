#!/usr/bin/python3

import os
import datetime
import random
import subprocess

def flip(p):
    return random.random() < p

def generate_test ( filenum, length=4, balancedProb=.75, path="./" ):

    braces = {
        0: ('<','>'),
        1: ('(',')'),
        2: ('[',']'),
        3: ('{','}'),
    }

    stack = []
    string = ""

    for _ in range(length):
        openNewBrace = bool(random.getrandbits(1))
        if openNewBrace:
            braceType = braces.get(random.randrange(4))
            stack.append(braceType)
            if flip(balancedProb):
                string += braceType[0]
        elif stack:
            if flip(balancedProb):
                string += stack.pop()[1]
    while stack:
        if flip(balancedProb):
            string += stack.pop()[1]

    # print (string)
    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write(string)


    stack = []
    allBalanced = True
    for char in string:
        if char=='<' or char=='(' or char=='[' or char=='{':
            stack.append(char)
        else:
            if stack:
                if char=='>':
                    allBalanced &= stack.pop()=='<'
                elif char==')':
                    allBalanced &= stack.pop()=='('
                elif char==']':
                    allBalanced &= stack.pop()=='['
                elif char=='}':
                    allBalanced &= stack.pop()=='{'
                else:
                    perror()
            else:
                allBalanced = False

    allBalanced &= stack==[]

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write("yes" if allBalanced else "no")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, length=4, balancedProb=0.75, path="./" )
    generate_test ( 1, length=4, balancedProb=0.5, path="./" )
    generate_test ( 2, length=8, balancedProb=0.9, path="./" )
    generate_test ( 3, length=8, balancedProb=0.25, path="./" )
    generate_test ( 4, length=16, balancedProb=0.9999, path="./" )
    generate_test ( 5, length=16, balancedProb=0.9, path="./" )

def test_balanced( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerString = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./balanced", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        resultString = result.stdout

        if verbose:
            print (' '.join(result.args))
            # print ("answerString")
            # print (answerString)
            # print ("resultString")
            # print (resultString)
        assert resultString == answerString, "The result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./balanced returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_balanced( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile balanced.c.")
        return score

    if test_balanced(0,path,verbose):
        score += 3
        if test_balanced(1,path,verbose):
            score += 3
            if test_balanced(2,path,verbose):
                score += 3
                if test_balanced(3,path,verbose):
                    score += 3
                    if test_balanced(4,path,verbose):
                        score += 3
                        if test_balanced(5,path,verbose):
                            score += 3

                            allpass = True
                            for filenum in range(6,12):
                                generate_test ( filenum, 256, 0.99, path )
                                allpass &= test_balanced(filenum,path,verbose)
                            if allpass:
                                score += 7

    print ("Score on balanced: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_balanced(verbose=True)
    exit()
