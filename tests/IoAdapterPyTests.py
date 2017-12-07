##
#
# File:    IoAdapterPyTests.py
# Author:  J. Westbrook
# Date:    01-Aug-2017
# Version: 0.001
#
# Updates:
#   2-Oct-2017 jdw  adjust block count on dictionary test
#   4-Oct-2017 jdw  verified the package IoAdapter default preference works.
#   7-Dec-2017 jdw  path all output files
##
"""
Test cases for reading and updating PDBx data files using Python Wrapper
IoAdapterCore wrapper which provides an API to the C++ CifFile class
library of file and dictionary tools that is conforms to our Native
Python library.
"""
from __future__ import absolute_import

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import sys
import os
import unittest
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    from mmcif import __version__
except Exception as e:
    sys.path.insert(0, os.path.dirname(HERE))
    from mmcif import __version__

#
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter
#
# How to use the default preference
# from mmcif.io import IoAdapter
from mmcif.io.PdbxReader import SyntaxError, PdbxError


class IoAdapterTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__pathPdbxDataFile = os.path.join(HERE, "data", "1kip.cif")
        self.__pathBigPdbxDataFile = os.path.join(HERE, "data", "1ffk.cif")
        self.__pathPdbxDictFile = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        self.__testBlockCount = 7350
        self.__pathErrPdbxDataFile = os.path.join(HERE, "data", "1bna-errors.cif")
        self.__pathQuotesPdbxDataFile = os.path.join(HERE, "data", "specialTestFile.cif")
        #
        self.__pathOutputPdbxFile = os.path.join(HERE, "test-output", "myPdbxOutputFile.cif")
        self.__pathQuotesOutputPdbxFile = os.path.join(HERE, "test-output", "myPdbxQuotesOutputFile.cif")
        self.__pathBigOutputDictFile = os.path.join(HERE, "test-output", "myDictOutputFile.cif")
        #
        self.__pathUnicodePdbxFile = os.path.join(HERE, "data", "unicode-test.cif")
        self.__pathCharRefPdbxFile = os.path.join(HERE, "data", "unicode-char-ref-test.cif")
        #
        self.__pathOutputUnicodePdbxFile = os.path.join(HERE, "test-output", "out-unicode-test.cif")
        self.__pathOutputCharRefPdbxFile = os.path.join(HERE, "test-output", "out-unicode-char-ref-test.cif")

        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testFileReaderUtf8(self):
        self.__testFileReader(self.__pathPdbxDataFile, enforceAscii=False)

    def testFileReaderBigUtf8(self):
        self.__testFileReader(self.__pathBigPdbxDataFile, enforceAscii=False)

    def testFileReaderQuotesUtf8(self):
        self.__testFileReader(self.__pathQuotesPdbxDataFile, enforceAscii=False)

    def testFileReaderUnicodeUtf8(self):
        self.__testFileReader(self.__pathUnicodePdbxFile, enforceAscii=False)

    def testFileReaderAscii(self):
        self.__testFileReader(self.__pathPdbxDataFile, enforceAscii=True)

    def testFileReaderBigAscii(self):
        self.__testFileReader(self.__pathBigPdbxDataFile, enforceAscii=True)

    def testFileReaderQuotesAscii(self):
        self.__testFileReader(self.__pathQuotesPdbxDataFile, enforceAscii=True)

    def __testFileReader(self, fp, enforceAscii=False):
        """Test case -  read PDBx file
        """
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(fp, enforceAscii=enforceAscii)
            logger.debug("Read %d data blocks" % len(containerList))
            self.assertEqual(len(containerList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testDictReaderUtf8(self):
        self.__testDictReader(self.__pathPdbxDictFile, enforceAscii=False)

    def testDictReaderAscii(self):
        self.__testDictReader(self.__pathPdbxDictFile, enforceAscii=False)

    def __testDictReader(self, fp, enforceAscii=False):
        """Test case -  read PDBx dictionary file
        """
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(fp, enforceAscii=enforceAscii)
            logger.debug("Read %d data blocks" % len(containerList))
            self.assertTrue(len(containerList) > self.__testBlockCount)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    #
    def testFileWIthSyntaxErrorHander1(self):
        self.__testFileReaderExceptionHandler1(self.__pathErrPdbxDataFile, enforceAscii=False)

    def testFileWIthSyntaxErrorHander2(self):
        self.__testFileReaderExceptionHandler1(self.__pathErrPdbxDataFile, enforceAscii=False)

    def testFileWIthUnicodeErrorHander2(self):
        self.__testFileReaderExceptionHandler2(self.__pathUnicodePdbxFile, enforceAscii=True)

    def __testFileReaderExceptionHandler1(self, fp, enforceAscii=False):
        """Test case -  read selected categories from PDBx file and handle exceptions
        """
        io = IoAdapter(raiseExceptions=True)
        self.assertRaises(SyntaxError, io.readFile, fp, enforceAscii=enforceAscii)

    def __testFileReaderExceptionHandler2(self, fp, enforceAscii=False):
        """Test case -  read selected categories from PDBx and handle exceptions
        """
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(fp, enforceAscii=enforceAscii)
            #
        except SyntaxError as e:
            logger.debug("Expected syntax failure")
            self.assertTrue(True)
        except PdbxError as e:
            logger.debug("Expected character encoding failure")
            self.assertTrue(True)
        except Exception as e:
            logger.exception("Unexpected exception %s " % type(e).__name__)
            self.fail('Unexpected exception raised: ' + str(e))
        else:
            self.fail('Expected exception not raised')

    def testFileReaderWriter(self):
        self.__testFileReaderWriter(self.__pathBigPdbxDataFile, self.__pathOutputPdbxFile)

    def testDictReaderWriter(self):
        self.__testFileReaderWriter(self.__pathPdbxDictFile, self.__pathBigOutputDictFile)

    def testFileReaderWriterQuotes(self):
        self.__testFileReaderWriter(self.__pathQuotesPdbxDataFile, self.__pathQuotesOutputPdbxFile)

    #
    def testFileReaderWriterUnicode(self):
        self.__testFileReaderWriter(self.__pathUnicodePdbxFile, self.__pathOutputUnicodePdbxFile, enforceAscii=False, cnvCharRefs=False)

    def testFileReaderWriterCharRef(self):
        self.__testFileReaderWriter(self.__pathCharRefPdbxFile, self.__pathOutputCharRefPdbxFile, enforceAscii=False, cnvCharRefs=True)

    def __testFileReaderWriter(self, ifp, ofp, **kwargs):
        """Test case -  read and then write PDBx file or dictionary
        """
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(ifp)
            logger.debug("Read %d data blocks" % len(containerList))
            ok = io.writeFile(ofp, containerList=containerList, **kwargs)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suiteFileReader():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderUtf8"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderBigUtf8"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderQuotesUtf8"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderAscii"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderBigAscii"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderQuotesAscii"))
    return suiteSelect


def suiteFileReaderExceptions():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileWIthSyntaxErrorHander1"))
    suiteSelect.addTest(IoAdapterTests("testFileWIthSyntaxErrorHander2"))
    #
    suiteSelect.addTest(IoAdapterTests("testFileWIthUnicodeErrorHander2"))
    return suiteSelect


def suiteDictReader():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testDictReaderAscii"))
    suiteSelect.addTest(IoAdapterTests("testDictReaderUtf8"))
    return suiteSelect


def suiteReaderUnicode():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderUnicodeUtf8"))
    return suiteSelect


def suiteReaderWriter():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriter"))
    suiteSelect.addTest(IoAdapterTests("testDictReaderWriter"))
    return suiteSelect


def suiteReaderWriterUnicode():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriterCharRef"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriterUnicode"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteFileReader()
        unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    if (True):
        mySuite = suiteDictReader()
        unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    if (True):
        mySuite = suiteFileReaderExceptions()
        unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    if (True):
        mySuite = suiteReaderUnicode()
        unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    if (True):
        mySuite = suiteReaderWriter()
        unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    if (True):
        mySuite = suiteReaderWriterUnicode()
        unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)
