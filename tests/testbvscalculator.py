#!/usr/bin/env python

"""Unit tests for diffpy.srreal.bvscalculator
"""

# version
__id__ = '$Id$'

import os
import unittest

# useful variables
thisfile = locals().get('__file__', 'file.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

from diffpy.srreal.bvscalculator import BVSCalculator
from diffpy.Structure import Structure

##############################################################################
class TestBVSCalculator(unittest.TestCase):

    def setUp(self):
        self.bvc = BVSCalculator()
        if not hasattr(self, 'rutile'):
            rutile_cif = os.path.join(testdata_dir, 'rutile.cif')
            TestBVSCalculator.rutile = Structure(filename=rutile_cif)
            # rutile.cif does not have charge data, we need to add them here
            iondict = {'Ti' : 'Ti4+',  'O' : 'O2-'}
            for a in self.rutile:  a.element = iondict[a.element]
        return


    def tearDown(self):
        return


    def test___init__(self):
        """check BVSCalculator.__init__()
        """
        self.assertEqual(1e-5, self.bvc.valenceprecision)
        bvc1 = BVSCalculator(valenceprecision=1e-4)
        self.assertEqual(1e-4, bvc1.valenceprecision)
        return


    def test___call__(self):
        """check BVSCalculator.__call__()
        """
        vcalc = self.bvc(self.rutile)
        self.assertEqual(len(self.rutile), len(vcalc))
        self.assertEqual(tuple(self.bvc.value()), tuple(vcalc))
        self.failUnless(vcalc[0] > 0)
        self.failUnless(vcalc[-1] < 0)
        self.assertAlmostEqual(0.0, sum(vcalc), 12)
        self.assertAlmostEqual(0.0, sum(self.bvc.valences()), 12)
        for vo, vc in zip(self.bvc.valences(), vcalc):
            self.failUnless(abs((vo - vc) / vo) < 0.1)
        return


    def test_bvdiff(self):
        """check BVSCalculator.bvdiff()
        """
        self.bvc(self.rutile)
        self.assertEqual(6, len(self.bvc.bvdiff()))
        # rutile is overbonded
        for bvd in self.bvc.bvdiff():
            self.failUnless(bvd < 0)
        return


    def test_bvmsdiff(self):
        """check BVSCalculator.bvmsdiff()
        """
        self.assertEqual(0, self.bvc.bvmsdiff())
        self.bvc(self.rutile)
        self.assertAlmostEqual(0.0158969, self.bvc.bvmsdiff(), 6)
        return


    def test_bvrmsdiff(self):
        """check BVSCalculator.bvrmsdiff()
        """
        from math import sqrt
        self.assertEqual(0, self.bvc.bvrmsdiff())
        self.bvc(self.rutile)
        self.failUnless(self.bvc.bvrmsdiff() > 0)
        self.assertAlmostEqual(sqrt(self.bvc.bvmsdiff()),
                self.bvc.bvrmsdiff(), 12)
        bvrmsd0 = self.bvc.bvrmsdiff()
        # check mixed occupancy
        rutilemix = Structure(self.rutile)
        for a in self.rutile:
            rutilemix.addNewAtom(a)
        for a in rutilemix:
            a.occupancy = 0.5
        self.bvc(rutilemix)
        self.assertEqual(12, len(self.bvc.value()))
        self.assertAlmostEqual(bvrmsd0, self.bvc.bvrmsdiff(), 12)
        return


    def test_eval(self):
        """check BVSCalculator.eval()
        """
        vcalc = self.bvc.eval(self.rutile)
        self.assertEqual(tuple(vcalc), tuple(self.bvc.value()))
        return


    def test_valences(self):
        """check BVSCalculator.valences()
        """
        self.bvc(self.rutile)
        self.assertEqual((4, 4, -2, -2, -2, -2),
                tuple(self.bvc.valences()))
        return

    def test_value(self):
        """check BVSCalculator.value()
        """
        self.assertEqual(0, len(self.bvc.value()))
        return

# End of class TestBVSCalculator

if __name__ == '__main__':
    unittest.main()

# End of file