#!/usr/bin/python3

import sys
from fullyAssociative import autograder as fullyAssociative_autograder
from directMapped import autograder as directMapped_autograder
from setAssociative import autograder as setAssociative_autograder
from cacheBlocking import autograder as cacheBlocking_autograder
from cacheOblivious import autograder as cacheOblivious_autograder

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

    total += fullyAssociative_autograder.grade_fullyAssociative ( path="tar_test/fullyAssociative/", verbose=False )
    total += directMapped_autograder.grade_directMapped ( path="tar_test/directMapped/", verbose=False )
    total += setAssociative_autograder.grade_setAssociative ( path="tar_test/setAssociative/", verbose=False )
    total += cacheBlocking_autograder.grade_cacheBlocking ( path="tar_test/cacheBlocking/", verbose=False )
    total += cacheOblivious_autograder.grade_cacheOblivious ( path="tar_test/cacheOblivious/", verbose=False )

    shutil.rmtree("tar_test")

else:

    total += fullyAssociative_autograder.grade_fullyAssociative ( path="fullyAssociative/", verbose=False )
    total += directMapped_autograder.grade_directMapped ( path="directMapped/", verbose=False )
    total += setAssociative_autograder.grade_setAssociative ( path="setAssociative/", verbose=False )
    total += cacheBlocking_autograder.grade_cacheBlocking ( path="cacheBlocking/", verbose=False )
    total += cacheOblivious_autograder.grade_cacheOblivious ( path="cacheOblivious/", verbose=False )

print ("Score on assignment: {} out of 150.".format(total))