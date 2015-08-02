import os
import unittest
from ansibledocgen.parser.ansiblecfg import AnsibleCfg

class TestAnsibleCfg(unittest.TestCase):
    def test_ansiblecfg(self):
        localdir = os.path.dirname(os.path.realpath(__file__))
        testfile = os.path.join(localdir, ".output/ansible.cfg")
        with open(testfile, "w") as f:
             f.write("\n roles_path = role1:role2\n")

        ansiblecfg = AnsibleCfg(os.path.dirname(testfile))

        assert( "roles_path" in ansiblecfg.settings )

        assert( "role1" in ansiblecfg.settings["roles_path"] )

        assert( "role2" in ansiblecfg.settings["roles_path"] )
