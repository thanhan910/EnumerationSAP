import unittest
import logging

from Enting1980 import G, g, enumerate_saps

OEIS_A002931 = [0, 1, 2, 7, 28, 124, 588, 2938, 15268, 81826, 449572, 2521270, 14385376, 83290424, 488384528, 2895432660, 17332874364, 104653427012, 636737003384, 3900770002646, 24045500114388, 149059814328236, 928782423033008, 5814401613289290, 36556766640745936]

class TestSAP2D(unittest.TestCase):
    def test_enumerate_saps(self):
        for length in range(4, 25, 2):
            with self.subTest(length=length):
                ans = enumerate_saps(length)
                expected_ans = 0 if (length <= 3 or length % 2 != 0) else OEIS_A002931[length // 2]
                self.assertEqual(ans, expected_ans, msg=f"length={length}, expected_ans={expected_ans}, ans={ans}")
                


if __name__ == "__main__":
    unittest.main()
