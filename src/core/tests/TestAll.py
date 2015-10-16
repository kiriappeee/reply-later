import unittest

from .TestReply import *
from .TestUsers import *
from .TestScheduler import *
from .TestMessageSender import *

#enable this test only for a full run. This is a long running test
#from .TestTweetAdapter import TestTweetAdapter

if __name__ == "__main__":
    unittest.main()
