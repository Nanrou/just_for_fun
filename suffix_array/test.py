from string import printable
from random import randint
import unittest
from suffix_array import SuffixArray, AnalyseCommonPart


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

        # print('\n', '-' * 20, '20000个随机字符', '-' * 20)
        _debug = False
        random_strings = ''.join([printable[randint(0, len(printable) - 1)] for _ in range(20000)])
        rd_sa = SuffixArray(random_strings, debug=_debug)
        rd_sa_dc3 = SuffixArray(random_strings, dc3=True, debug=_debug)
        for _ in range(100):
            i = randint(1, len(rd_sa.sa) - 1)
            self.assertEqual(rd_sa.sa[i], rd_sa_dc3.sa[i])
            self.assertTrue(random_strings[rd_sa.sa[i]:] > random_strings[rd_sa.sa[i - 1]:])

        # print('\n', '-' * 20, '测试文本（长度9390）', '-' * 20)
        with open('test.txt', 'r', encoding='utf-8') as rf:
            text = rf.read()
            rd_sa = SuffixArray(text[:200], debug=_debug)
            rd_sa_dc3 = SuffixArray(text[:200], dc3=True, debug=_debug)
            for _ in range(100):
                i = randint(1, len(rd_sa.sa) - 1)
                self.assertEqual(rd_sa.sa[i], rd_sa_dc3.sa[i])
                self.assertTrue(text[rd_sa.sa[i]:] > text[rd_sa.sa[i - 1]:])

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


class TestAnalyseCommonPart(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tt = [
            "小源科技获年度“最佳企业服务商”殊荣,",
            "小源科技获年度“最佳企业服务商”殊荣, 短信公众号将成新流量风口",
            "小源科技获年度“最佳企业服务商”殊荣, 短信公众号将成新流量风",
            "小源科技获年度“最佳企业服务商”殊荣, 推短信公众号或将成为新",
            "小源科技获年度“最佳企业服务商”殊荣, 短信公众号或将成为新风口",
        ]

        cls.sa_double = AnalyseCommonPart(tt * 100)
        cls.sa_dc3 = AnalyseCommonPart(tt * 100)

    def test_basic_logic(self):
        pass

    def test_analyze(self):
        self.assertEqual(self.sa_dc3.analyze(), self.sa_double.analyze())


if __name__ == '__main__':
    unittest.main()
