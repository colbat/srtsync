#!/usr/bin/python

import os
import re
import unittest
from srtsync import sync

class TestSrtSync(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.currdir = os.path.dirname(__file__)
        self.inputfile = os.path.join(self.currdir,'subtitles.srt')
        self.outputfile = os.path.join(self.currdir,'out.srt')
        self.regex = r'(\d{2}:\d{2}:\d{2},\d{3})'


    @classmethod
    def tearDownClass(self):
        os.remove(self.outputfile)


    def test_sync_diff_positive(self):
        sync(self.inputfile, self.outputfile, 1100)

        synced_file = open(self.outputfile, 'r')
        content = synced_file.read()
        result = re.findall(self.regex, content)
        
        self.assertEqual(result[0], '00:00:03,386')
        self.assertEqual(result[1], '00:00:10,350')
        self.assertEqual(result[2], '00:10:10,470')
        self.assertEqual(result[3], '00:10:13,048')
        self.assertEqual(result[4], '01:00:12,708')
        self.assertEqual(result[5], '01:00:14,042')
        self.assertEqual(result[6], '02:02:19,848')
        self.assertEqual(result[7], '02:02:21,416')

        synced_file.close()


    def test_sync_diff_negative(self):
        sync(self.inputfile, self.outputfile, -1100)

        synced_file = open(self.outputfile, 'r')
        content = synced_file.read()
        result = re.findall(self.regex, content)
        
        self.assertEqual(result[0], '00:00:01,186')
        self.assertEqual(result[1], '00:00:08,150')
        self.assertEqual(result[2], '00:10:08,270')
        self.assertEqual(result[3], '00:10:10,848')
        self.assertEqual(result[4], '01:00:10,508')
        self.assertEqual(result[5], '01:00:11,842')
        self.assertEqual(result[6], '02:02:17,648')
        self.assertEqual(result[7], '02:02:19,216')

        synced_file.close()


    def test_sync_range_positive(self):
        sync(self.inputfile, self.outputfile, '00:00:02,286', '00:00:03,386')

        synced_file = open(self.outputfile, 'r')
        content = synced_file.read()
        result = re.findall(self.regex, content)
        
        self.assertEqual(result[0], '00:00:03,386')
        self.assertEqual(result[1], '00:00:10,350')
        self.assertEqual(result[2], '00:10:10,470')
        self.assertEqual(result[3], '00:10:13,048')
        self.assertEqual(result[4], '01:00:12,708')
        self.assertEqual(result[5], '01:00:14,042')
        self.assertEqual(result[6], '02:02:19,848')
        self.assertEqual(result[7], '02:02:21,416')

        synced_file.close()


    def test_sync_range_negative(self):
        sync(self.inputfile, self.outputfile, '00:00:02,286', '00:00:01,186')

        synced_file = open(self.outputfile, 'r')
        content = synced_file.read()
        result = re.findall(self.regex, content)
        
        self.assertEqual(result[0], '00:00:01,186')
        self.assertEqual(result[1], '00:00:08,150')
        self.assertEqual(result[2], '00:10:08,270')
        self.assertEqual(result[3], '00:10:10,848')
        self.assertEqual(result[4], '01:00:10,508')
        self.assertEqual(result[5], '01:00:11,842')
        self.assertEqual(result[6], '02:02:17,648')
        self.assertEqual(result[7], '02:02:19,216')

        synced_file.close()


    def test_sync_bad_timings_with_range(self):
        self.assertRaises(Exception, sync, self.inputfile, 
                          self.outputfile, 1100, '00:00:02,286', '00:00:03,386')


    def test_sync_no_timings(self):
        self.assertRaises(Exception, sync, self.inputfile, self.outputfile)