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


"""Local utilities helpful for tweaking interfaces to boost python classes.
"""

# module version
__id__ = "$Id$"

import copy

# Routines -------------------------------------------------------------------

def propertyFromExtDoubleAttr(attrname, doc):
    '''Create property wrapper to a DoubleAttr in C++ extension object.

    attrname -- string name of the double attribute
    doc      -- docstring for the Python class property

    Return a property object.
    '''
    def fget(self):
        return self._getDoubleAttr(attrname)
    def fset(self, value):
        self._setDoubleAttr(attrname, value)
        return
    rv = property(fget, fset, doc=doc)
    return rv


def setattrFromKeywordArguments(obj, **kwargs):
    '''Set attributes of the obj according to keywork arguments.
    For example:    setattrFromKeywordArguments(obj, qmax=24, scale=2)
    This is a shared helper function used by __init__ and __call__.

    kwargs   -- one or more keyword arguments

    No return value.
    Raise ValueError for invalid keyword argument.
    '''
    for n, v in kwargs.iteritems():
        if not hasattr(obj, n):
            emsg = "Unknown attribute %r" % n
            raise ValueError(emsg)
        setattr(obj, n, v)
    return


def _wrapAsRegisteredUnaryFunction(cls, regname, fnc, **dbattrs):
    '''Helper function for wrapping Python function as PDFBaseline or
    PDFEnvelope functor.  Not intended for direct usage, this function
    is rather called from makePDFBaseline or makePDFEnvelope wrappers.

    cls      -- the functor class for wrapping the Python function
    regname  -- string name for registering the function in the global
                registry of cls functors.  This will be the string
                identifier for the createByType factory.
    fnc      -- Python function of a floating point argument and optional
                float parameters.  The parameters need to be registered as
                dbattrs in the functor class.  The function fnc
                must be picklable and it must return a float.
    dbattrs  -- optional float parameters of the wrapped function.
                These will be registered as double attributes in the
                functor class.  The wrapped function must be callable as
                fnc(x, **dbattrs).

    Return an instance of the functor class.
    '''
    class RegisteredUnaryFunction(cls):

        def create(self):
            '''Create new instance of the same type as self.
            '''
            return RegisteredUnaryFunction()

        def clone(self):
            '''Return a new duplicate instance of self.
            '''
            return copy.copy(self)

        def type(self):
            '''Unique string identifier of this functor type.  The string
            is used for class registration and as an argument for the
            createByType function.

            Return string identifier.
            '''
            return regname

        def __call__(self, x):
            '''Evaluate this functor at x.
            '''
            if dbattrs:
                kw = dict([(n, self._getDoubleAttr(n))
                        for n in self._namesOfWritableDoubleAttributes()])
                rv = fnc(x, **kw)
            else:
                rv = fnc(x)
            return rv

        def __init__(self):
            cls.__init__(self)
            for n, v in dbattrs.items():
                setattr(self, n, v)
                self._registerDoubleAttribute(n)
            return

    # End of class RegisteredUnaryFunction

    RegisteredUnaryFunction()._registerThisType()
    rv = RegisteredUnaryFunction.createByType(regname)
    assert type(rv) is RegisteredUnaryFunction
    return rv

# End of file
