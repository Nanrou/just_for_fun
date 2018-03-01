import unittest
from suffix_array import SuffixArray


class TestSuffixArray(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sa1 = SuffixArray('aabaaaab')
        cls.sa2 = SuffixArray('ABRACADABRA!')

    def test_basic_logic(self):
        self.assertEqual(self.sa1.rank, [3, 5, 7, 0, 1, 2, 4, 6])
        self.assertEqual(self.sa1.height, [3, 2, 3, 1, 2, 0, 1])

        self.assertEqual(self.sa2.sa, [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2])
        self.assertEqual(self.sa2.height, [0, 1, 4, 1, 1, 0, 3, 0, 0, 0, 2])

    def test_lcp_of_two_suffix(self):
        self.assertEqual(self.sa1.lcp_of_two_suffix(1, 4), 'a')
        self.assertEqual(self.sa1.lcp_of_two_suffix(4, 1), 'a')
        self.assertEqual(self.sa1.lcp_of_two_suffix(4, 4), 'aaab')

        self.assertEqual(self.sa2.lcp_of_two_suffix(1, 4), '')
        self.assertEqual(self.sa2.lcp_of_two_suffix(4, 1), '')
        self.assertEqual(self.sa2.lcp_of_two_suffix(4, 4), 'CADABRA!')

    def test_longest_repeated_sub_string(self):
        self.assertEqual(self.sa1.longest_repeated_sub_string(), 'aaa')
        self.assertEqual(self.sa2.longest_repeated_sub_string(), 'ABRA')

    def test_unique_longest_repeated_sub_string(self):
        self.assertEqual(self.sa1.unique_longest_repeated_sub_string(), 'aa')
        self.assertEqual(self.sa2.unique_longest_repeated_sub_string(), 'ABRA')

    def test_count_different_sub_string(self):
        self.assertEqual(self.sa1.count_different_sub_string(), 29)
        self.assertEqual(self.sa2.count_different_sub_string(), 87)


if __name__ == '__main__':
    unittest.main()
