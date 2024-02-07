#!/usr/bin/python3

import os
import datetime
import random
import networkx as nx
# import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, isTree, nodes, edges, path="./" ):

    if isTree:
        G = nx.random_tree(nodes)
    else:
        G = nx.gnm_random_graph(nodes, edges)

    # nx.draw(G, with_labels=True, font_weight='bold')
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
        try:
            cycle = nx.find_cycle(G)
        except nx.NetworkXNoCycle:
            cycle = None
        outfile.write("no" if cycle else "yes")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, True, 2, 2, path="./"  )
    generate_test ( 1, True, 4, 16, path="./"  )
    generate_test ( 2, True, 8, 32, path="./"  )
    generate_test ( 3, False, 2, 2, path="./"  )
    generate_test ( 4, False, 4, 16, path="./"  )
    generate_test ( 5, False, 8, 32, path="./"  )

def test_isTree ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerStr = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./isTree", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        resultStr = result.stdout.strip()

        if verbose:
            print (' '.join(result.args))
            # print ("answerStr")
            # print (answerStr)
            # print ("resultStr")
            # print (resultStr)
        assert answerStr == resultStr, "Your answer doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./isTree returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_isTree( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile isTree.c.")
        return score

    if test_isTree(0,path,verbose):
        score += 1
        if test_isTree(1,path,verbose):
            score += 1
            if test_isTree(2,path,verbose):
                score += 1
                if test_isTree(3,path,verbose):
                    score += 1
                    if test_isTree(4,path,verbose):
                        score += 1
                        if test_isTree(5,path,verbose):
                            score += 1
                            for filenum in range(6,25):
                                isTree = bool(random.getrandbits(1))
                                generate_test ( filenum, isTree, 16, 256, path )
                                if test_isTree(filenum,path,verbose):
                                    score += 1

    print ("Score on isTree: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_isTree(verbose=True)
    exit()
