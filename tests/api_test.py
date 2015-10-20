import unittest
import tempfile

from docit import db
from docit.webapp import app
from docit.api import api

class DocitTestCase(unittest.TestCase):
    def setUp(self):
        
