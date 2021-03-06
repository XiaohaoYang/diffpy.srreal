/*****************************************************************************
*
* diffpy.srreal     by DANSE Diffraction group
*                   Simon J. L. Billinge
*                   (c) 2011 Trustees of the Columbia University
*                   in the City of New York.  All rights reserved.
*
* File coded by:    Pavol Juhas
*
* See AUTHORS.txt for a list of people who contributed.
* See LICENSE.txt for license information.
*
******************************************************************************
*
* Shared declarations of wrapper functions that convert to Python types.
* This file is always included from srreal_converters.hpp.
*
* $Id$
*
*****************************************************************************/

#ifndef SRREAL_CONVERTERS_IPP_INCLUDED
#define SRREAL_CONVERTERS_IPP_INCLUDED

namespace srrealmodule {

// definitions of shared template wrappers

DECLARE_PYARRAY_METHOD_WRAPPER(value, value_asarray)
DECLARE_PYARRAY_METHOD_WRAPPER(distances, distances_asarray)
DECLARE_PYARRAY_METHOD_WRAPPER(sites0, sites0_asarray)
DECLARE_PYARRAY_METHOD_WRAPPER(sites1, sites1_asarray)
DECLARE_PYARRAY_METHOD_WRAPPER(directions, directions_asarray)
DECLARE_PYCHARARRAY_METHOD_WRAPPER(types0, types0_aschararray)
DECLARE_PYCHARARRAY_METHOD_WRAPPER(types1, types1_aschararray)

}   // namespace srrealmodule

#endif  // SRREAL_CONVERTERS_IPP_INCLUDED
