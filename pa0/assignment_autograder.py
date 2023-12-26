#!/usr/bin/python3

import sys
from euclidEuler import autograder as euclidEuler_autograder

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

    total += euclidEuler_autograder.grade_euclidEuler ( path="tar_test/euclidEuler/", verbose=True )

    shutil.rmtree("tar_test")

else:

    total += euclidEuler_autograder.grade_euclidEuler ( path="euclidEuler/", verbose=True )

print ("Score on assignment: {} out of 15.".format(total))