'''
These are the unit tests for the partitioning module functions
_______________________________________________________________________________
Created on Feb 4, 2015

@author: Kevin Paul <kpaul@ucar.edu>
'''
import unittest
import partitioning
import numpy
from os import linesep

def test_info_msg(name, data, index, size, actual, expected):
    spcr = ' ' * len(name)
    msg = ''.join([linesep,
                   name, ' - Data: ', str(data), linesep,
                   spcr, ' - Index/Size: ', str(index), '/', str(size), linesep,
                   spcr, ' - Actual:   ', str(actual), linesep,
                   spcr, ' - Expected: ', str(expected)])
    return msg


class partitionTests(unittest.TestCase):
    '''
    Unit tests for the partitioning module
    '''

    def setUp(self):
        data = [numpy.arange(3), numpy.arange(5), numpy.arange(7)]
        indices_sizes = [(0, 1), (1, 3), (5, 9)]
        self.inputs = []
        for d in data:
            for (i, s) in indices_sizes:
                self.inputs.append((d, i, s))

    def tearDown(self):
        pass

    def testOutOfBounds(self):
        self.assertRaises(IndexError, partitioning.PartitionFunction(), [1, 2, 3], 3, 3)
        self.assertRaises(IndexError, partitioning.PartitionFunction(), [1, 2, 3], 7, 3)

    def testPartitionFunction(self):
        for inp in self.inputs:
            pfunc = partitioning.PartitionFunction()
            actual = pfunc(*inp)
            expected = inp[0]
            msg = test_info_msg('PartitionFunction', inp[0], inp[1], inp[2], actual, expected)
            print msg
            numpy.testing.assert_array_equal(actual, expected, msg)

    def testEquallength(self):
        results = [numpy.arange(3), numpy.array([1]), numpy.array([]),
                   numpy.arange(5), numpy.array([2, 3]), numpy.array([]),
                   numpy.arange(7), numpy.array([3, 4]), numpy.array([5])]
        for (ii, inp) in enumerate(self.inputs):
            pfunc = partitioning.EqualLength()
            actual = pfunc(*inp)
            expected = results[ii]
            msg = test_info_msg('EqualLength', inp[0], inp[1], inp[2], actual, expected)
            print msg
            numpy.testing.assert_array_equal(actual, expected, msg)

    def testEqualStride(self):
        for inp in self.inputs:
            pfunc = partitioning.EqualStride()
            actual = pfunc(*inp)
            expected = inp[0][inp[1]::inp[2]]
            msg = test_info_msg('EqualStride', inp[0], inp[1], inp[2], actual, expected)
            print msg
            numpy.testing.assert_array_equal(actual, expected, msg)

    def testSortedStride(self):
        for inp in self.inputs:
            weights = numpy.array([(20 - i) for i in inp[0]])
            pfunc = partitioning.SortedStride()
            data = numpy.dstack((inp[0], weights))[0]
            actual = pfunc(data, inp[1], inp[2])
            expected = inp[0][::-1]
            expected = expected[inp[1]::inp[2]]
            msg = test_info_msg('SortedStride', data, inp[1], inp[2], actual, expected)
            print msg
            numpy.testing.assert_array_equal(actual, expected, msg)

    def testWeightBalanced(self):
        results = [{0, 1, 2}, {1}, set(),
                   {3, 2, 4, 1, 0}, {1}, set(),
                   {3, 2, 4, 1, 5, 0, 6}, {3, 6}, {4}]
        for (ii, inp) in enumerate(self.inputs):
            weights = numpy.array([(3 - i) ** 2 for i in inp[0]])
            pfunc = partitioning.WeightBalanced()
            data = numpy.dstack((inp[0], weights))[0]
            actual = set(pfunc(data, inp[1], inp[2]))
            expected = results[ii]
            msg = test_info_msg('WeightBalanced', data, inp[1], inp[2], actual, expected)
            print msg
            self.assertEqual(actual, expected, msg)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBasicInt']
    unittest.main()