# Copyright (c) 2016-2017 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import filecmp
import os
import pytest
import subprocess
import sys


tests_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(tests_dir, 'resources')
antlr = os.getenv('ANTLR')


@pytest.mark.parametrize('args_cache', [
    ('--cache=none', ),
    ('--cache=config', ),
    ('--cache=content', ),
])
@pytest.mark.parametrize('args_parser', [
    (),
    ('--parser=java', ),
])
@pytest.mark.parametrize('args_hdd_star', [
    (),
    ('--no-hdd-star', ),
])
@pytest.mark.parametrize('args_squeeze', [
    (),
    ('--no-squeeze-tree', ),
])
@pytest.mark.parametrize('args_skip_unremovable_tokens', [
    (),
    ('--no-skip-unremovable-tokens', ),
])
class TestCli:

    @pytest.mark.parametrize('test, inp, exp, grammar, rule', [
        ('test-json-obj-arr-foo.sh', 'inp-obj-arr.json', 'exp-obj-arr-foo.json', 'JSON.g4', 'json'),
        ('test-json-obj-arr-bar.sh', 'inp-obj-arr.json', 'exp-obj-arr-bar.json', 'JSON.g4', 'json'),
        ('test-json-obj-arr-baz.sh', 'inp-obj-arr.json', 'exp-obj-arr-baz.json', 'JSON.g4', 'json'),
        ('test-json-obj-arr-87.sh', 'inp-obj-arr.json', 'exp-obj-arr-87.json', 'JSON.g4', 'json'),
    ])
    def test_cli(self, test, inp, exp, grammar, rule, tmpdir, args_cache, args_parser, args_hdd_star, args_squeeze, args_skip_unremovable_tokens):
        out_dir = '%s' % tmpdir
        cmd = (sys.executable, '-m', 'picireny')\
              + ('--test=' + test, '--input=' + inp, '--out=' + out_dir) \
              + ('--log-level=DEBUG', ) \
              + ('--grammar=' + grammar, '--start-rule=' + rule)
        if antlr:
              cmd += ('--antlr=' + antlr, )
        cmd += args_cache
        cmd += args_parser
        cmd += args_hdd_star
        cmd += args_squeeze
        cmd += args_skip_unremovable_tokens
        proc = subprocess.Popen(cmd, cwd=resources_dir)
        proc.communicate()
        assert proc.returncode == 0
        assert filecmp.cmp(os.path.join(out_dir, inp), os.path.join(resources_dir, exp))
