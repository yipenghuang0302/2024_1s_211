#!/usr/bin/python3

import os
import datetime
import random
import subprocess

from string import ascii_uppercase

def generate_test ( filenum, jobs=4, timeslots=16, path="./" ):

    jobs_by_end_time = {}

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        # write the total number of jobs to be scheduled
        infile.write( "{}\n".format( jobs ) )
        # write the last possible timeslot
        infile.write( "{}\n".format( timeslots ) )

        for _,job in zip( range(jobs), ascii_uppercase ):

            end = random.randrange(0,timeslots)

            if not end in jobs_by_end_time:
                jobs_by_end_time[end] = []
            jobs_by_end_time[end].append(job)

            infile.write( "{} {}\n".format( job, end ) )

        # print(jobs_by_end_time)

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        # iterator over the dictionary's value sorted in keys.
        for end in sorted (jobs_by_end_time):
            for job in jobs_by_end_time[end]:
                outfile.write( "{}\n".format(job) )

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, jobs=2, timeslots=8, path="./" )
    generate_test ( 1, jobs=4, timeslots=16, path="./" )
    generate_test ( 2, jobs=8, timeslots=32, path="./" )
    generate_test ( 3, jobs=16,timeslots=64, path="./" )

def test_sortJobs ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerList = []
            for line in outfile.read().split('\n'):
                if line:
                    answerList.append(line)
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./sortJobs", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=4).total_seconds(),
        )

        resultList = []
        for line in result.stdout.split():
            resultList.append(line)

        if verbose:
            print (' '.join(result.args))
            # print ("answer")
            # print (answerList)
            # print ("result")
            # print (result.stdout)
        assert resultList == answerList, "The job schedule result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./sortJobs returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_sortJobs( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile sortJobs.c.")
        return score

    if test_sortJobs(0,path,verbose):
        score += 4
        if test_sortJobs(1,path,verbose):
            score += 4
            if test_sortJobs(2,path,verbose):
                score += 4
                if test_sortJobs(3,path,verbose):
                    score+= 4
                    allPass = True
                    for filenum in range(4,16):
                        generate_test ( filenum, jobs=4, timeslots=16, path=path )
                        allPass &= test_sortJobs(filenum,path,verbose)
                    if allPass:
                        score+=4

    print ("Score on sortJobs: {} out of 20.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_sortJobs(verbose=True)
    exit()
