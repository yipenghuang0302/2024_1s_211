#!/usr/bin/python3

import os
import datetime
import random
import networkx as nx
# import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, nodes, edges, path="./" ):

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    # nx.draw(G, with_labels=True, font_weight='bold', pos=nx.spring_layout(G))
    # plt.savefig("{}tests/test{}.png".format(path,filenum))
    # plt.close()

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write("{}\n".format(nodes))
        A = nx.adjacency_matrix(G).toarray()
        for row in A:
            for col in row:
                infile.write("{} ".format(col))
            infile.write("\n")

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        for cycle in nx.recursive_simple_cycles(G):
            for graphNode in cycle:
                outfile.write(str(graphNode))
                outfile.write(' ')
            outfile.write('\n')

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 2, 3, path="./"  )
    generate_test ( 1, 4, 6, path="./"  )
    generate_test ( 2, 6, 9, path="./"  )
    generate_test ( 3, 8, 12, path="./"  )
    generate_test ( 4, 10, 15, path="./"  )
    generate_test ( 5, 12, 18, path="./"  )

def test_findCycle ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerCycles = []
            for line in outfile.readlines():
                answerCycles.append(list(map(int, line.split())))
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./findCycle", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        if not answerCycles:
            assert result.stdout.strip() == "DAG", 'Expected "DAG" printout indicating no cycles found.'
        else:
            resultCycle = list(map(int, result.stdout.split()))

            resultInAnswer = False
            def rotate(l, n):
                return l[-n:] + l[:-n]
            for rot in range(len(resultCycle)):
                if rotate(resultCycle,rot) in answerCycles:
                    resultInAnswer = True

            if verbose:
                print (' '.join(result.args))
                # print ("answerCycles")
                # print (answerCycles)
                # print ("resultCycle")
                # print (resultCycle)
            assert resultInAnswer, "Your answer doesn't match answers/answer{}.txt.".format(filenum)

        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./findCycle returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_findCycle( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile findCycle.c.")
        return score

    if test_findCycle(0,path,verbose):
        score += 1
        if test_findCycle(1,path,verbose):
            score += 1
            if test_findCycle(2,path,verbose):
                score += 1
                if test_findCycle(3,path,verbose):
                    score += 1
                    if test_findCycle(4,path,verbose):
                        score += 1
                        if test_findCycle(5,path,verbose):
                            score += 1

                            for filenum in range(6,25):
                                generate_test ( filenum, 16, 32, path )
                                if test_findCycle(filenum,path,verbose):
                                    score += 1

    print ("Score on findCycle: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_findCycle(verbose=True)
    exit()
