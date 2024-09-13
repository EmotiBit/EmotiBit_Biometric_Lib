import unittest
import timestamp_converter as tsc

class TestTimestampConverterMethods(unittest.TestCase):

    def test_calculateSlopeWithGoodValues(self):
        sourceOneFirstTaps = [10, 20, 30]
        sourceTwoFirstTaps = [10, 15, 20]
        sourceOneSecondTaps = [50, 60, 70]
        sourceTwoSecondTaps = [50, 55, 60]

        self.assertEqual(tsc.calculate_slope(sourceOneFirstTaps, sourceOneSecondTaps, sourceTwoFirstTaps, sourceTwoSecondTaps),
                         1,
                         "Slope was not calculated correctly")
        
    def test_calculateSlopeWithMismatchedFirstLengths(self):
        sof = [1, 2, 3]
        stf = [1, 2]
        sos = [4, 6, 8]
        sts = [6, 8, 10]

        self.assertIsNone(tsc.calculate_slope(sof, sos, stf, sts),
                          "Did not detect that the length of first set of taps did not match")
        
    def test_calculateSlopeWithMismatchedSecondLengths(self):
        sof = [1, 2, 3]
        stf = [1, 2, 8]
        sos = [4, 8]
        sts = [6, 8, 10]

        self.assertIsNone(tsc.calculate_slope(sof, sos, stf, sts),
                          "Did not detect that the length of second set of taps did not match")

    def test_calculateBWithGoodValues(self):
        so = [1, 2, 3]
        st = [3, 4, 5]

        self.assertEqual(tsc.calculate_b(1, so, st),
                         -2,
                         "Did not properly calculate y-intercept")
        
    def test_calculateBWithMismatchedLengths(self):
        so = [1, 2, 3]
        st = [2, 3]

        self.assertIsNone(tsc.calculate_b(1, so, st),
                          "Did not detect mismatched lengths")




if __name__ == "__main__":
    unittest.main()