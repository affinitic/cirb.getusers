# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting

import cirb.getusers

GETUSERS = PloneWithPackageLayer(
	    zcml_filename="configure.zcml",
	    zcml_package=cirb.getusers,
	    additional_z2_products=(),
	    gs_profile_id='cirb.getusers:default',
	    name="GETUSERS")

NOVAC_INTEGRATION = IntegrationTesting(
	    bases=(GETUSERS,), name="GETUSERS_INTEGRATION")


NOVAC_FUNCTIONAL = FunctionalTesting(
	    bases=(GETUSERS,), name="GETUSERS_FUNCTIONAL")