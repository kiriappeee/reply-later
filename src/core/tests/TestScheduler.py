import unittest
from datetime import datetime, timezone, timedelta
from crontab import CronTab
from unittest.mock import Mock
from ..scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    def setUp(self):
        c = CronTab(user=True)
        c.remove_all()
        c.write()

    def tearDown(self):
        c = CronTab(user=True)
        c.remove_all()
        c.write()

    def test_scheduleAddedCorrectly(self):
        expectedSchedule = '0 7 1 1 * /bin/sh /replylater/src/core/runmessage.sh --id=1 --data=sqllite # 1'
        tz = timezone(timedelta(hours=5, minutes=30))
        d = datetime(year=2022, month=1, day=1, hour=12, minute=30, tzinfo=tz)
        Scheduler.scheduleReply(1, d)
        c = CronTab(user=True)
        iter = c.find_comment('1')
        jobs = [i for i in iter]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(str(jobs[0]), expectedSchedule)
        
    def test_scheduleUpdatedCorrectly(self):
        expectedSchedule = '0 7 1 1 * /bin/sh /replylater/src/core/runmessage.sh --id=1 --data=sqllite # 1'
        tz = timezone(timedelta(hours=5, minutes=30))
        d = datetime(year=2022, month=1, day=1, hour=12, minute=30, tzinfo=tz)
        Scheduler.scheduleReply(1, d)
        c = CronTab(user=True)
        iter = c.find_comment('1')
        jobs = [i for i in iter]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(str(jobs[0]), expectedSchedule)

        d = datetime(year=2022, month=2, day=1, hour=12, minute=30, tzinfo=tz)
        expectedSchedule = '0 7 1 2 * /bin/sh /replylater/src/core/runmessage.sh --id=1 --data=sqllite # 1'
        Scheduler.updateReply(1, d)
        c = CronTab(user=True)
        iter = c.find_comment('1')
        jobs = [i for i in iter]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(str(jobs[0]), expectedSchedule)

        tz = timezone(timedelta(hours=4, minutes=0))
        d = datetime(year=2022, month=2, day=1, hour=12, minute=30, tzinfo=tz)
        expectedSchedule = '30 8 1 2 * /bin/sh /replylater/src/core/runmessage.sh --id=1 --data=sqllite # 1'
        Scheduler.updateReply(1, d)
        c = CronTab(user=True)
        iter = c.find_comment('1')
        jobs = [i for i in iter]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(str(jobs[0]), expectedSchedule)

    def test_scheduleRemovedCorrectly(self):
        expectedSchedule = '0 7 1 1 * /bin/sh /replylater/src/core/runmessage.sh --id=1 --data=sqllite # 1'
        tz = timezone(timedelta(hours=5, minutes=30))
        d = datetime(year=2022, month=1, day=1, hour=12, minute=30, tzinfo=tz)
        Scheduler.scheduleReply(1, d)
        c = CronTab(user=True)
        iter = c.find_comment('1')
        jobs = [i for i in iter]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(str(jobs[0]), expectedSchedule)
        Scheduler.removeReply(1)
        c = CronTab(user=True)
        iter = c.find_comment('1')
        jobs = [i for i in iter]
        self.assertEqual(len(jobs), 0)


if __name__ == "__main__":
    unittest.main()
