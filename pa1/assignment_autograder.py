#!/usr/bin/python3

import sys
from greedyScheduling import autograder as greedyScheduling_autograder
from editDistance import autograder as editDistance_autograder
from balanced import autograder as balanced_autograder

total = 0

if len( sys.argv ) > 1:

    import tarfile, os, shutil

    with tarfile.open(sys.argv[1]) as tarball:
        def is_within_directory(directory, target):

            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)

            prefix = os.path.commonprefix([abs_directory, abs_target])

            return prefix == abs_directory

        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")

            tar.extractall(path, members, numeric_owner=numeric_owner) 


        safe_extract(tarball, "tar_test")

    total += greedyScheduling_autograder.grade_greedyScheduling ( path="tar_test/greedyScheduling/", verbose=True )
    total += editDistance_autograder.grade_editDistance ( path="tar_test/editDistance/", verbose=True )
    total += balanced_autograder.grade_balanced ( path="tar_test/balanced/", verbose=True )

    shutil.rmtree("tar_test")

else:

    total += greedyScheduling_autograder.grade_greedyScheduling ( path="greedyScheduling/", verbose=True )
    total += editDistance_autograder.grade_editDistance ( path="editDistance/", verbose=True )
    total += balanced_autograder.grade_balanced ( path="balanced/", verbose=True )

print ("Score on assignment: {} out of 75.".format(total))