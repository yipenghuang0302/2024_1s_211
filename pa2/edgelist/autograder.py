#!/usr/bin/python3

import os
import datetime
import scipy
import networkx as nx
# import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, nodes, edges, path="./" ):

    G = nx.gnm_random_graph(nodes, edges)
    A = nx.adjacency_matrix(G).toarray()

    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.savefig("{}tests/test{}.png".format(path,filenum))
    # plt.close()

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write("{}\n".format(nodes))
        for row in A:
            for col in row:
                infile.write("{} ".format(col))
            infile.write("\n")

    with open("{}answers/answer{}.txt".format(path,filenum), "wb") as outfile:
        nx.write_edgelist(G, outfile, data=False)

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 2, 2, path="./"  )
    generate_test ( 1, 4, 4, path="./"  )
    generate_test ( 2, 6, 6, path="./"  )
    generate_test ( 3, 8, 8, path="./"  )
    generate_test ( 4, 12, 12, path="./"  )
    generate_test ( 5, 14, 14, path="./"  )

def test_edgelist ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerGraph = nx.read_edgelist(outfile)
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./edgelist", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        lines = result.stdout.split('\n')
        resultGraph = nx.parse_edgelist(lines)

        if verbose:
            print (' '.join(result.args))
            # print ("answerGraph")
            # print (answerGraph)
            # print ("resultGraph")
            # print (resultGraph)
        assert answerGraph.nodes == resultGraph.nodes, "The nodes in your graph don't match the nodes in the graph in answers/answer{}.txt.".format(filenum)
        assert answerGraph.edges == resultGraph.edges, "The edge list doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./edgelist returned an error.")
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

def grade_edgelist( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile queue.c.")
        return score

    if test_edgelist(0,path,verbose):
        score += 1
        if test_edgelist(1,path,verbose):
            score += 1
            if test_edgelist(2,path,verbose):
                score += 1
                if test_edgelist(3,path,verbose):
                    score += 1
                    if test_edgelist(4,path,verbose):
                        score += 1
                        if test_edgelist(5,path,verbose):
                            score += 1
                            for filenum in range(6,25):
                                generate_test ( filenum, 16, 32, path=path )
                                if test_edgelist(filenum,path,verbose):
                                    score += 1                    

    print ("Score on edgelist: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_edgelist(verbose=True)
    exit()
