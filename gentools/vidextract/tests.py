import unittest
import numpy
import enc

class TestVidextract(unittest.TestCase):
    def setUp(self):
        self.bmp1 = numpy.array([1, 1, 1, 2, 2, 2, 3, 3, 3, 4], dtype=numpy.uint8)
        self.bmp2 = numpy.array([1, 1, 4, 4, 4, 2, 3, 2, 3, 4], dtype=numpy.uint8)

    def _apply_srle_to_bmp(self, srle, bmp1):
        bmp2 = bmp1.copy()
        for val in srle:
            for (off, cnt) in srle[val]:
                for idx in xrange(off, off + cnt):
                    bmp2[idx] = val
        return bmp2

    def test_rle(self):
        dlist = enc.runlength_enc(self.bmp1)
        self.assertEqual(dlist, [(0, 1, 3), (3, 2, 3), (6, 3, 3), (9, 4, 1)])

    def test_diff1(self):
        dlist = enc.runlength_delta_enc(self.bmp1, self.bmp2)
        self.assertEqual(dlist, [(2, 4, 3), (7, 2, 1)])

    def test_diff2(self):
        dlist = enc.runlength_delta_enc(self.bmp1, self.bmp2)
        srle = enc.runlength_sort(dlist)
        outbmp = self._apply_srle_to_bmp(srle, self.bmp1)
        self.assertTrue(numpy.array_equal(outbmp, self.bmp2))

    def test_diff3(self):
        rbmp1 = numpy.random.randint(0, 16, 100000)
        rbmp2 = numpy.random.randint(0, 16, 100000)
        dlist = enc.runlength_delta_enc(rbmp1, rbmp2)
        srle = enc.runlength_sort(dlist)
        outbmp = self._apply_srle_to_bmp(srle, rbmp1)
        self.assertTrue(numpy.array_equal(outbmp, rbmp2))


if __name__ == '__main__':
    unittest.main()
