#!/usr/bin/env python
##############################################################################
#
# diffpy.srreal     by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Pavol Juhas
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################


"""class Attributes  -- wrapper to C++ class diffpy::Attributes
    A base to PairQuantity and quite a few other classes.
"""

# module version
__id__ = "$Id$"
__all__ = ['Attributes']

from diffpy.srreal.srreal_ext import Attributes

# Inject the __getattr__ and __setattr__ methods to the Attributes class

def __getattr__(self, name):
    '''Lookup a C++ double attribute if standard Python lookup fails.

    Raise AttributeError if C++ double attribute does not exist.
    '''
    try:
        rv = self._getDoubleAttr(name)
    except Exception, e:
        raise AttributeError(e)
    return rv

Attributes.__getattr__ = __getattr__


def __setattr__(self, name, value):
    '''Assign to C++ double attribute if it exists.  Use standard Python
    attribute assignment otherwise.
    '''
    if self._hasDoubleAttr(name):
        self._setDoubleAttr(name, value)
    else:
        object.__setattr__(self, name, value)
    return

Attributes.__setattr__ = __setattr__

# End of file
