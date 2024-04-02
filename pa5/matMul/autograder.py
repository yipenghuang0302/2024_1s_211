#!/usr/bin/python3

import os
import datetime
import random
import numpy
from scipy.stats import unitary_group
import subprocess

def generate_test ( n, path="./" ):

    matrix_a = unitary_group.rvs(n)
    matrix_b = unitary_group.rvs(n)
    matrix_c = numpy.matmul( matrix_a, matrix_b )

    with open("{}tests/matrix_a_{}x{}.txt".format(path,n,n), "w") as infile:
        infile.write("{}\n".format(n))
        for i in range (n):
            for j in range (n):
                infile.write("{} ".format(matrix_a[i][j]))
            infile.write("\n")

    with open("{}tests/matrix_b_{}x{}.txt".format(path,n,n), "w") as infile:
        infile.write("{}\n".format(n))
        for i in range (n):
            for j in range (n):
                infile.write("{} ".format(matrix_b[i][j]))
            infile.write("\n")

    with open("{}answers/matrix_c_{}x{}.txt".format(path,n,n), "w") as outfile:
        for i in range (n):
            for j in range (n):
                outfile.write("{} ".format(matrix_c[i][j]))
            outfile.write("\n")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    for i in range(2,17):
        generate_test ( i )

def test_matMul ( n, path="./", verbose=False ):

    try:
        with open("{}answers/matrix_c_{}x{}.txt".format(path,n,n), "r") as outfile:
            answer = []
            for line in outfile.read().split('\n'):
                row = []
                for string in line.split(' '):
                    if string != '':
                        row.append(complex(string))
                if line != '':
                    answer.append(row)
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/matrix_c_{}x{}.txt missing".format(n,n))

    try:
        result = subprocess.run(
            ['./matMul', "tests/matrix_a_{}x{}.txt".format(n,n), "tests/matrix_b_{}x{}.txt".format(n,n)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='ASCII',
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        resultlist = []
        for line in result.stdout.split('\n'):
            row = []
            for string in line.split(' '):
                if string != '':
                    row.append(complex(string))
            if line != '':
                resultlist.append(row)

        # print ("answer")
        # print (answer)
        # print ("resultlist")
        # print (resultlist)
        assert numpy.allclose(resultlist, answer), "The matrix multiplication result doesn't match answers/matrix_c_{}x{}.txt.".format(n,n)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./matMul returned non-zero exit status.")
    except ValueError as e:
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (e.args[0])

    return False

def grade_matMul( path='./', verbose=False ):

    score = 0

    try:
        subprocess.run( ['make', '-B'], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile matMul.")
        return score

    for i in range(2,17):
        if test_matMul(i,path,verbose):
            score += 2
        else:
            break

    print ("Score on matMul: {} out of 30.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_matMul(verbose=True)
    exit()
