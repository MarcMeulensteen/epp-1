#!/usr/bin/env python

import unittest
from epp1 import *

class TestEpp(unittest.TestCase):

    def setUp(self):
        pass
 
    def test_eprom_type(self):
        set_eprom_type("B964")
        self.assertEqual( get_eprom_type(), 'B964' )
        
    def test_start_address(self):
        set_start_address("00FF")
        self.assertEqual( get_start_address(), '00FF' )

    def test_set_end_address_before_start_address(self):
        set_start_address("00FF")
        set_end_address("00FE")
        
    def test_is_empty(self):
        self.assertEqual( is_empty(), False )        

if __name__ == '__main__':
    unittest.main()
