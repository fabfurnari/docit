import unittest
import tempfile

import docit

class DocitTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, docit.app.config['DATABASE'] = tempfile.mkstemp()
        print "testing: %s" % docit.app.config['TESTING']
        self.app = docit.app.test_client()
        docit.init_db()

if __name__ == '__main__':
    unittest.main()
