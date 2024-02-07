#!/usr/bin/python3

import os
import datetime
import random
import networkx as nx
from networkx.algorithms import approximation as approx
# import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, isCyclic, nodes, edges, path="./" ):

    while True:
        if isCyclic:
            G = nx.gnm_random_graph(nodes, edges)
        else:
            G = nx.random_tree(nodes)
        if nx.is_connected(G): # ensure connected graph
            break

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

    with open("{}queries/query{}.txt".format(path,filenum), "w") as qfile:

        source = random.randrange(nodes)
        qfile.write("{}\n".format(source))

        target = source
        while target == source:
            target = random.randrange(nodes) # make sure source and target are different nodes
        qfile.write("{}\n".format(target))

    with open("{}edgelists/edgelist{}.txt".format(path,filenum), "wb") as efile:
        nx.write_edgelist(G, efile, data=False)

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("queries", exist_ok=True)
    os.makedirs("edgelists", exist_ok=True)

    generate_test ( 0, False, 2, 2, path="./" ) # acyclic
    generate_test ( 1, False, 4, 16, path="./" ) # acyclic
    generate_test ( 2, False, 16, 256, path="./" ) # acyclic
    generate_test ( 3, True, 2, 2, path="./" ) # cyclic
    generate_test ( 4, True, 4, 16, path="./" ) # cyclic
    generate_test ( 5, True, 16, 256, path="./" ) # cyclic

def test_solveMaze ( filenum, path="./", verbose=False ):

    try:
        with open("{}queries/query{}.txt".format(path,filenum), "r") as qfile:
            source = int(qfile.readline())
            target = int(qfile.readline())
        with open("{}edgelists/edgelist{}.txt".format(path,filenum), "r") as edgelistfile:
            mazeGraph = nx.read_edgelist(edgelistfile,nodetype=int)
    except EnvironmentError: # parent of IOError, OSError
        print ("edgelists/edgelist{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./solveMaze", "tests/test{}.txt".format(filenum), "queries/query{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        lines = result.stdout.split('\n')
        resultGraph = nx.parse_edgelist(lines,nodetype=int)

        if verbose:
            print (' '.join(result.args))
            # print ("answerlist")
            # print (answerlist)
            # print ("resultlist")
            # print (resultlist)
        for edge in resultGraph.edges:
            # print(edge)
            assert edge in mazeGraph.edges, "The edge {} is not part of the original graph.".format(edge)
        assert(approx.local_node_connectivity(resultGraph,source,target)==1), "The edges you returned do not connect the source and target nodes listed in queries/query{}.txt.".format(filenum)
        return True

    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./solveMaze returned an error.")
    except TypeError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_solveMaze( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile solveMaze.c.")
        return score

    if test_solveMaze(0,path,verbose):
        score += 1
        if test_solveMaze(1,path,verbose):
            score += 1
            if test_solveMaze(2,path,verbose):
                score += 1
                if test_solveMaze(3,path,verbose):
                    score += 1
                    if test_solveMaze(4,path,verbose):
                        score += 1
                        if test_solveMaze(5,path,verbose):
                            score += 1

                            for filenum in range(6,25):
                                isCyclic = bool(random.getrandbits(1))
                                generate_test ( filenum, isCyclic, 32, 64, path ) # cyclic
                                if test_solveMaze(filenum,path,verbose):
                                    score += 1

    print ("Score on solveMaze: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_solveMaze(verbose=True)
    exit()
