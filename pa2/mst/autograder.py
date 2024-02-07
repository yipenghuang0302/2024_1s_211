#!/usr/bin/python3

import os
import datetime
import random
import networkx as nx
# import matplotlib.pyplot as plt
import subprocess

def generate_test ( filenum, nodes, edges, path="./" ):

    while True:
        G = nx.gnm_random_graph(nodes, edges)
        if nx.is_connected(G): # ensure connected graph
            break

    for (u,v,w) in G.edges(data=True):
        w['weight'] = random.random()

    # nx.draw(G, with_labels=True, font_weight='bold', pos=nx.spring_layout(G))
    # nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))
    # plt.savefig("{}tests/test{}.png".format(path,filenum))
    # plt.close()

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write("{}\n".format(nodes))

        A = nx.adjacency_matrix(G).toarray()
        for row in A:
            for col in row:
                infile.write("{} ".format(col))
            infile.write("\n")

    mst = nx.minimum_spanning_tree(G)
    with open("{}answers/answer{}.txt".format(path,filenum), "wb") as outfile:
        nx.write_edgelist(mst, outfile, data=False)

    # nx.draw(mst, with_labels=True, font_weight='bold', pos=nx.spring_layout(mst))
    # nx.draw_networkx_edge_labels(mst, pos=nx.spring_layout(mst))
    # plt.savefig("{}answers/answer{}.png".format(path,filenum))
    # plt.close()

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, 2, 4, path="./"  )
    generate_test ( 1, 3, 6, path="./"  )
    generate_test ( 2, 4, 8, path="./"  )
    generate_test ( 3, 5, 10, path="./"  )
    generate_test ( 4, 6, 12, path="./"  )
    generate_test ( 5, 7, 14, path="./"  )

def test_mst ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerGraph = nx.read_edgelist(outfile,nodetype=int)
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./mst", "tests/test{}.txt".format(filenum)],
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
            # print ("answerGraph")
            # print (answerGraph)
            # print ("resultGraph")
            # print (resultGraph)
        assert answerGraph.nodes == resultGraph.nodes, "The nodes in your graph don't match the graph in answers/answer{}.txt.".format(filenum)
        assert answerGraph.edges == resultGraph.edges, "The edge list doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./mst returned an error.")
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

def grade_mst( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile queue.c.")
        return score

    if test_mst(0,path,verbose):
        score += 1
        if test_mst(1,path,verbose):
            score += 1
            if test_mst(2,path,verbose):
                score += 1
                if test_mst(3,path,verbose):
                    score += 1
                    if test_mst(4,path,verbose):
                        score += 1
                        if test_mst(5,path,verbose):
                            score += 1
                            for filenum in range(6,25):
                                generate_test ( filenum, 16, 32, path )
                                if test_mst(filenum,path,verbose):
                                    score += 1

    print ("Score on mst: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_mst(verbose=True)
    exit()
