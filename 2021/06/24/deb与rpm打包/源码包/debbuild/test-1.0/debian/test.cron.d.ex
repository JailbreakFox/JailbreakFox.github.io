#
# Regular cron jobs for the test package
#
0 4	* * *	root	[ -x /usr/bin/test_maintenance ] && /usr/bin/test_maintenance
