import unittest

from Enting1980 import G, g, enumerate_saps


class TestSAP2D(unittest.TestCase):
    def test_enumerate_saps(self):
        ANS = {
            4: 1,
            6: 2,
            8: 7,
            10: 28,
            12: 124,
            14: 588,
            16: 2_938,
            18: 15_268,
            20: 81_826,
            22: 449_572,
            24: 2_521_270,
            26: 14_385_376,
            28: 83_290_424,
            30: 488_384_528,
            32: 2_895_432_660,
            34: 17_332_874_364,
            36: 104_653_427_012,
            38: 636_737_003_384,
        }
        for length, ans in ANS.items():
            # print success message if test passes, else print error message
            with self.subTest(length=length):
                self.assertEqual(enumerate_saps(length), ans)



if __name__ == "__main__":
    unittest.main()
