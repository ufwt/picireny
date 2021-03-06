# Copyright (c) 2017 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import logging

from picire import AbstractDD, ConfigCache

logger = logging.getLogger(__name__)


class EmptyDD(AbstractDD):
    """
    Special DD variant that *does* test the empty configuration (and nothing
    else).
    """

    def __init__(self, test, *, cache=None):
        """
        Initialize an EmptyDD object.

        :param test: A callable tester object.
        :param cache: Cache object to use.
        """
        AbstractDD.__init__(self, test, None, cache=cache)

    def ddmin(self, config):
        """
        Return a 1-minimal failing subset of the initial configuration, and also
        test the empty configuration while doing so.

        Note: The initial configuration is expected to be of size 1, thus the
        1-minimal failing subset is always its trivial subset: either itself or
        the empty configuration.

        :param config: The initial configuration that will be reduced.
        :return: 1-minimal failing configuration.
        """

        assert len(config) == 1

        logger.debug('dd(%r) ...', config)

        outcome = self._dd(config)

        logger.debug('dd(%r) = %r', config, outcome)

        return outcome

    def _dd(self, config):
        # assert self.test(config, 'assert') == self.FAIL

        emptyset = []
        config_id = 'empty'

        logger.info('Run: trying 0.')

        outcome = self.lookup_cache(emptyset, config_id) or self.test(emptyset, config_id)
        if outcome == self.FAIL:
            logger.info('Reduced to 0 units.')
            logger.debug('New config: %r.', emptyset)

            logger.info('Done.')
            return emptyset

        logger.info('Done.')
        return config
