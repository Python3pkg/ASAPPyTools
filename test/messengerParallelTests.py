'''
Unit tests for the Messenger class (parallel only)

-----------------------
Created on Jan 7, 2015

@author: kpaul
'''
import unittest
import messenger


class MessengerParallelTests(unittest.TestCase):
    '''
    Parallel Messenger unit tests.
    '''

    def test_init(self):
        msngr = messenger.MPIMessenger()
        self.assertIsInstance(msngr, messenger.Messenger,
                              'Failed to create class instance')
        self.assertEqual(msngr._mpi_rank, msngr.get_rank(),
                         'Rank is wrong after initialization')
        self.assertEqual(msngr._mpi_size, msngr.get_size(),
                         'Size is wrong after initialization')
        self.assertEqual(msngr._is_master, (0 == msngr.get_rank()),
                         'Is_master is wrong after initialization')
        self.assertEqual(msngr.verbosity, 1,
                         'Verbosity is wrong after initialization')

    def test_partition(self):
        msngr = messenger.MPIMessenger()
        data = [i for i in range(msngr.get_size())]
        p_data = msngr.partition(data)
        self.assertListEqual(p_data, [msngr.get_rank()],
                         'Parallel partition is wrong')

    def test_is_master(self):
        msngr = messenger.MPIMessenger()
        if msngr.get_rank() == 0:
            self.assertTrue(msngr.is_master(),
                            'Parallel messenger should be master')
        else:
            self.assertFalse(msngr.is_master(),
                            'Parallel messenger should not be master')

    def test_sum_list(self):
        msngr = messenger.MPIMessenger()
        data = [1, 2, 3, 4]
        size = msngr.get_size()
        msngr_sum = msngr.reduce(data, op='sum')
        self.assertEqual(msngr_sum, sum(data) * size,
                        'Parallel messenger list sum not working')

    def test_sum_dict(self):
        msngr = messenger.MPIMessenger()
        data = {'a': 1, 'b': [2, 6], 'c': 3}
        size = msngr.get_size()
        rslt = {'a': 1 * size, 'b': 8 * size, 'c': 3 * size}
        msngr_sum = msngr.reduce(data, op='sum')
        self.assertDictEqual(msngr_sum, rslt,
                        'Parallel messenger dict sum not working')

    def test_max_list(self):
        msngr = messenger.MPIMessenger()
        rank = msngr.get_rank()
        data = [rank + i for i in range(4)]
        rslt = (msngr.get_size() - 1) + 3
        msngr_max = msngr.reduce(data, op='max')
        self.assertEqual(msngr_max, rslt,
                        'Parallel messenger list max not working')

    def test_max_dict(self):
        msngr = messenger.MPIMessenger()
        data = {'a': 1, 'b': [2, 7], 'c': 3}
        rslt = {'a': 1, 'b': 7, 'c': 3}
        msngr_max = msngr.reduce(data, op='max')
        self.assertDictEqual(msngr_max, rslt,
                        'Parallel messenger dict max not working')

    def test_print_once(self):
        msngr = messenger.MPIMessenger()
        msg = 'TEST - ONCE - Parallel'
        msngr.prinfo(msg, vlevel=0, master=True)

    def test_print_all(self):
        msngr = messenger.MPIMessenger()
        msg = 'TEST - ALL - Parallel'
        msngr.prinfo(msg, vlevel=0, master=False)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
