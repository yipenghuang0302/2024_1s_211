#!/usr/bin/python3

import os
import datetime
import random
import subprocess
import string

def generate_test ( filenum, path="./" ):

    read_address = random.randrange(4)

    set_0_valid = random.getrandbits(1)
    set_0_tag = random.getrandbits(1)
    set_0_block = random.randrange(1<<8)

    set_1_valid = random.getrandbits(1)
    set_1_tag = random.getrandbits(1)
    set_1_block = random.randrange(1<<8)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        infile.write("{}\n".format(read_address))

        infile.write("{}\n".format(set_0_valid))
        infile.write("{}\n".format(set_0_tag))
        infile.write("{}\n".format(set_0_block))

        infile.write("{}\n".format(set_1_valid))
        infile.write("{}\n".format(set_1_tag))
        infile.write("{}\n".format(set_1_block))

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        set_1 = 0b1 & read_address>>0

        valid = set_1_valid if set_1 else set_0_valid
        tag = set_1_tag if set_1 else set_0_tag
        block = set_1_block if set_1 else set_0_block

        search_tag = 0b1 & read_address>>1
        match = search_tag == tag
        match_valid = valid and match

        block_match = block if match else 0

        read_byte = block_match

        outfile.write("read_hit" + " = {}\n".format( int(match_valid) ))
        outfile.write("read_byte" + " = {}\n".format( read_byte ))

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, path="./" )
    generate_test ( 1, path="./" )
    generate_test ( 2, path="./" )
    generate_test ( 3, path="./" )
    generate_test ( 4, path="./" )
    generate_test ( 5, path="./" )

def test_directMapped ( filenum, path="./", verbose=False ):

    try:
        with open("{}tests/test{}.txt".format(path,filenum), "r") as infile:
            read_address = infile.readline().strip()

            set_0_valid = infile.readline().strip()
            set_0_tag = infile.readline().strip()
            set_0_block = infile.readline().strip()

            set_1_valid = infile.readline().strip()
            set_1_tag = infile.readline().strip()
            set_1_block = infile.readline().strip()

    except EnvironmentError: # parent of IOError, OSError
        print ("tests/test{}.txt missing".format(filenum))

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerDict = {}
            for line in outfile.read().split("\n"):
                if line != "":
                    words = line.split(" ")
                    if words[0] not in ["Read"]:
                        var = words[0]
                        val = words[2]
                        answerDict[var] = val
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["../circuitSimulator", "directMapped.v", read_address,
            set_0_valid, set_0_tag, set_0_block,
            set_1_valid, set_1_tag, set_1_block,
            ],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        resultDict = {}
        for line in result.stdout.split("\n"):
            if line != "":
                words = line.split(" ")
                if words[0] not in ["Read"]:
                    var = words[0]
                    val = words[2]
                    resultDict[var] = val

        if verbose:
            print (' '.join(result.args))
            print ("answer")
            print (answerDict)
            print ("result")
            print (result.stdout)
        assert resultDict['read_hit'] == answerDict['read_hit'], "The circuit simulation result doesn't match answers/answer{}.txt.".format(filenum)
        if resultDict['read_hit'] == '1':
            assert resultDict['read_byte'] == answerDict['read_byte'], "The circuit simulation result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ../circuitSimulator returned non-zero exit status.")
    # except ValueError as e:
    #     print (result.stdout)
    #     print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_directMapped( path="./", verbose=False ):

    score = 0

    if test_directMapped(0,path,verbose):
        score += 0.5
        if test_directMapped(1,path,verbose):
            score += 0.5
            if test_directMapped(2,path,verbose):
                score += 0.5
                if test_directMapped(3,path,verbose):
                    score += 0.5
                    if test_directMapped(4,path,verbose):
                        score += 0.5
                        if test_directMapped(5,path,verbose):
                            score += 0.5
                            for filenum in range(6,50):
                                generate_test ( filenum, path=path )
                                if test_directMapped(filenum,path,verbose):
                                    score += 0.5
                                else:
                                    break

    print ("Score on directMapped: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_directMapped(verbose=True)
    exit()
