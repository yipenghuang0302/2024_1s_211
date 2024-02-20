#!/usr/bin/python3

import sys
from binSub import autograder as binSub_autograder
from anyToAny import autograder as anyToAny_autograder
from rootFinder import autograder as rootFinder_autograder
from binToFloat import autograder as binToFloat_autograder
from doubleToBin import autograder as doubleToBin_autograder
from floatMul import autograder as floatMul_autograder

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

    total += binSub_autograder.grade_binSub ( path="tar_test/binSub/", verbose=False )
    total += anyToAny_autograder.grade_anyToAny ( path="tar_test/anyToAny/", verbose=False )
    total += rootFinder_autograder.grade_rootFinder ( path="tar_test/rootFinder/", verbose=False )
    total += binToFloat_autograder.grade_binToFloat ( path="tar_test/binToFloat/", verbose=False )
    total += doubleToBin_autograder.grade_doubleToBin ( path="tar_test/doubleToBin/", verbose=False )
    total += floatMul_autograder.grade_floatMul ( path="tar_test/floatMul/", verbose=False )

    shutil.rmtree("tar_test")

else:

    total += binSub_autograder.grade_binSub ( path="binSub/", verbose=False )
    total += anyToAny_autograder.grade_anyToAny ( path="anyToAny/", verbose=False )
    total += rootFinder_autograder.grade_rootFinder ( path="rootFinder/", verbose=False )
    total += binToFloat_autograder.grade_binToFloat ( path="binToFloat/", verbose=False )
    total += doubleToBin_autograder.grade_doubleToBin ( path="doubleToBin/", verbose=False )
    total += floatMul_autograder.grade_floatMul ( path="floatMul/", verbose=False )

print ("Score on assignment: {} out of 150.".format(total))