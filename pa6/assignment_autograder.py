#!/usr/bin/python3

import sys
from comparator import autograder as comparator_autograder
from sevenSegmentDisplayE import autograder as sevenSegmentDisplayE_autograder
from sevenSegmentDisplayC import autograder as sevenSegmentDisplayC_autograder
from sevenSegmentDisplay import autograder as sevenSegmentDisplay_autograder
from fullyAssociative import autograder as fullyAssociative_autograder
from setAssociative import autograder as setAssociative_autograder
from binSub import autograder as binSub_autograder

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

    total += comparator_autograder.grade_comparator ( path="tar_test/comparator/", verbose=False )
    total += sevenSegmentDisplayE_autograder.grade_sevenSegmentDisplayE ( path="tar_test/sevenSegmentDisplayE/", verbose=False )
    total += sevenSegmentDisplayC_autograder.grade_sevenSegmentDisplayC ( path="tar_test/sevenSegmentDisplayC/", verbose=False )
    total += sevenSegmentDisplay_autograder.grade_sevenSegmentDisplay ( path="tar_test/sevenSegmentDisplay/", verbose=False )
    total += fullyAssociative_autograder.grade_fullyAssociative ( path="tar_test/fullyAssociative/", verbose=False )
    total += setAssociative_autograder.grade_setAssociative ( path="tar_test/setAssociative/", verbose=False )
    total += binSub_autograder.grade_binSub ( path="tar_test/binSub/", verbose=False )

    shutil.rmtree("tar_test")

else:

    total += comparator_autograder.grade_comparator ( path="comparator/", verbose=False )
    total += sevenSegmentDisplayE_autograder.grade_sevenSegmentDisplayE ( path="sevenSegmentDisplayE/", verbose=False )
    total += sevenSegmentDisplayC_autograder.grade_sevenSegmentDisplayC ( path="sevenSegmentDisplayC/", verbose=False )
    total += sevenSegmentDisplay_autograder.grade_sevenSegmentDisplay ( path="sevenSegmentDisplay/", verbose=False )
    total += fullyAssociative_autograder.grade_fullyAssociative ( path="fullyAssociative/", verbose=False )
    total += setAssociative_autograder.grade_setAssociative ( path="setAssociative/", verbose=False )
    total += binSub_autograder.grade_binSub ( path="binSub/", verbose=False )

print ("Score on assignment: {} out of 150.".format(total))