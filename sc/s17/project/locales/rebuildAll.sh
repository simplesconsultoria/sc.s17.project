#!/bin/bash
# kudos to Products.Ploneboard for the base for this file
# ensure that when something is wrong, nothing is broken more than it should...
set -e

# first, create some pot containing anything
i18ndude rebuild-pot --pot sc.s17.project.pot --create sc.s17.project --merge manual.pot ..

# finally, update the po files
i18ndude sync --pot sc.s17.project.pot  `find . -iregex '.*sc.s17.project\.po$'|grep -v plone`

