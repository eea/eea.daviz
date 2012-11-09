#!/usr/bin/env bash
cd $(dirname $0)
domain=eea
i18ndude rebuild-pot --pot $domain.pot --create $domain ../../
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po
