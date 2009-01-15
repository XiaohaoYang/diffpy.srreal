/***********************************************************************
* Short Title: unit tests for R3linalg
*
* Comments:
*
* $Id$
*
* <license text>
***********************************************************************/

#include <stdexcept>
#include <cppunit/TestFixture.h>
#include <cppunit/extensions/HelperMacros.h>

#include "R3linalg.hpp"

using namespace std;
using namespace diffpy;
using diffpy::R3::MatricesAlmostEqual;
using diffpy::R3::VectorsAlmostEqual;

class TestR3linalg : public CppUnit::TestFixture
{

    CPPUNIT_TEST_SUITE(TestR3linalg);
    CPPUNIT_TEST(test_norm);
    CPPUNIT_TEST(test_dot);
    CPPUNIT_TEST(test_cross);
    CPPUNIT_TEST(test_product);
    CPPUNIT_TEST_SUITE_END();

private:

    static const double precision = 1.0e-12;

public:

    void test_norm()
    {
	R3::Vector v1, v2;
	v1 = 3.0, 4.0, 0.0;
	v2 = 0.67538115798129, 0.72108424545413, 0.15458914063315;
	CPPUNIT_ASSERT_DOUBLES_EQUAL(5.0, R3::norm(v1), precision);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(1.0, R3::norm(v2), precision);
    }


    void test_dot()
    {
	R3::Vector v1, v2;
	v1 = -0.97157650177843, 0.43206192654604, 0.56318686427062;
	v2 = -0.04787719419083, 0.55895824010234, -0.34472910285751;
	double dot_v1v2 = 0.09387402846316;
	CPPUNIT_ASSERT_DOUBLES_EQUAL(dot_v1v2, R3::dot(v1, v2), precision);
    }


    void test_cross()
    {
	R3::Vector v1, v2, v1xv2;
	v1 = -0.55160549932839, -0.58291452407504,  0.12378162306543;
	v2 =  0.60842511285200, -0.97946444006248, -0.02828214306095;
	v1xv2 = 0.13772577008800,  0.05971126233738,  0.89493780662849;
	CPPUNIT_ASSERT(VectorsAlmostEqual(v1xv2,
		    R3::cross(v1, v2), precision) );
    }


    void test_product()
    {
        R3::Matrix M;
        R3::Vector v, prod_Mv, prod_vM;
        M = 0.459631856585519, 0.726448904209060, 0.085844209317482,
            0.806838095807669, 0.240116998848762, 0.305032463662873,
            0.019487235483683, 0.580605953831255, 0.726077578738676 ;
        v = 0.608652521912322, 0.519716469261062, 0.842577887601566;
        prod_Mv = 0.729633980805669, 0.872890409522479, 0.925388343907868;
        prod_vM = 0.715502648789536, 1.056153454546559, 0.822556602046019;
        CPPUNIT_ASSERT(VectorsAlmostEqual(prod_Mv,
                    R3::product(M, v), precision) );
        CPPUNIT_ASSERT(VectorsAlmostEqual(prod_vM,
                    R3::product(v, M), precision) );
    }


};

// Registers the fixture into the 'registry'
CPPUNIT_TEST_SUITE_REGISTRATION(TestR3linalg);

// End of file
