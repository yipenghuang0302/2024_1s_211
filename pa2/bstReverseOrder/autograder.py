#!/usr/bin/python3

import os
import datetime
import random
import subprocess

class BinarySearchTreeNode:

    def __init__(self):
        self.l = None
        self.data = None
        self.r = None

    def insert(self, val):
        if self.data == None:
            self.data = val
        if val < self.data:
            if not self.l:
                self.l = BinarySearchTreeNode()
            self.l.insert(val)
        elif val == self.data:
            pass
        else:
            if not self.r:
                self.r = BinarySearchTreeNode()
            self.r.insert(val)

    def reverse_order_traversal(self):
        string = self.r.reverse_order_traversal() if self.r else ""
        string += str(self.data)
        string += " "
        string += self.l.reverse_order_traversal() if self.l else ""
        return string

def generate_test ( filenum, length, path="./" ):

    root = BinarySearchTreeNode()

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        for _ in range (length):
            val = random.randrange(2*length)
            root.insert(val)
            infile.write("{} ".format(val))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        outfile.write(root.reverse_order_traversal())

def generate_test_suite():

    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("answers"):
        os.mkdir("answers")

    generate_test ( 0, 1 )
    generate_test ( 1, 2 )
    generate_test ( 2, 4 )
    generate_test ( 3, 8 )

def test_bstReverseOrder ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answer = [ int(num) for num in outfile.read().split() ]
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./bstReverseOrder", "tests/test{}.txt".format(filenum)],
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
            # print ("answer")
            # print (answer)
            # print ("resultlist")
            # print (resultlist)
        assert resultlist == answer, "The breadth first traversal of the bst doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./bstReverseOrder returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_bstReverseOrder( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile bstReverseOrder.c.")
        return score

    if test_bstReverseOrder(0,path,verbose):
        score += 5
        if test_bstReverseOrder(1,path,verbose):
            score += 5
            if test_bstReverseOrder(2,path,verbose):
                score += 5
                if test_bstReverseOrder(3,path,verbose):
                    score += 5

                    allpass = True
                    for filenum in range(4,8):
                        generate_test ( filenum, 32, path )
                        allpass &= test_bstReverseOrder(filenum,path,verbose)
                    if allpass:
                        score += 5

    print ("Score on bstReverseOrder: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_bstReverseOrder(verbose=True)
    exit()
