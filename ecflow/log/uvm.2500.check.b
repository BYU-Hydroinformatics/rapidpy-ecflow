# 4.12.0
defs_state MIGRATE state>:complete flag:message
edit ECF_MICRO '%' # server
edit ECF_HOME '/home/michael/host_share/rapid_run/ecflow' # server
edit ECF_JOB_CMD '%ECF_JOB% 1> %ECF_JOBOUT% 2>&1' # server
edit ECF_KILL_CMD 'kill -15 %ECF_RID%' # server
edit ECF_STATUS_CMD 'ps --pid %ECF_RID% -f > %ECF_JOB%.stat 2>&1' # server
edit ECF_URL_CMD '${BROWSER:=firefox} -new-tab %ECF_URL_BASE%/%ECF_URL%' # server
edit ECF_URL_BASE 'https://confluence.ecmwf.int' # server
edit ECF_URL 'display/ECFLOW/ecflow+home' # server
edit ECF_LOG '/home/michael/host_share/rapid_run/ecflow/uvm.2500.ecf.log' # server
edit ECF_INTERVAL '60' # server
edit ECF_LISTS '/home/michael/host_share/rapid_run/ecflow/ecf.lists' # server
edit ECF_CHECK '/home/michael/host_share/rapid_run/ecflow/uvm.2500.check' # server
edit ECF_CHECKOLD '/home/michael/host_share/rapid_run/ecflow/uvm.2500.check.b' # server
edit ECF_CHECKINTERVAL '120' # server
edit ECF_CHECKMODE 'CHECK_ON_TIME' # server
edit ECF_TRIES '2' # server
edit ECF_VERSION '4.12.0' # server
edit ECF_PORT '2500' # server
edit ECF_NODE '%ECF_HOST%' # server
edit ECF_HOST 'uvm' # server
edit ECF_CHECK_CMD 'ps --pid %ECF_RID% -f' # server
edit ECF_PID '2715' # server
history / MSG:[00:07:32 21.2.2019] --restart :michaelMSG:[00:09:14 21.2.2019] --restart :michaelMSG:[00:11:52 21.2.2019] --restart :michaelMSG:[00:12:12 21.2.2019] --restart :michaelMSG:[16:33:05 21.2.2019] --restart :michaelMSG:[16:39:37 21.2.2019] --restart :michaelMSG:[16:40:37 21.2.2019] --restart :michaelMSG:[16:42:35 21.2.2019] --restart :michaelMSG:[16:43:08 21.2.2019] --restart :michaelMSG:[16:45:14 21.2.2019] --restart :michaelMSG:[17:39:20 21.2.2019] --restart :michaelMSG:[17:44:31 21.2.2019] --restart :michaelMSG:[17:53:57 21.2.2019] --restart :michaelMSG:[18:23:35 21.2.2019] --restart :michaelMSG:[18:32:13 21.2.2019] --restart :michaelMSG:[18:34:24 21.2.2019] --restart :michaelMSG:[18:38:10 21.2.2019] --restart :michaelMSG:[18:40:29 21.2.2019] --restart :michaelMSG:[18:40:54 21.2.2019] --restart :michaelMSG:[20:44:41 21.2.2019] --restart :michael
history /run_rapid MSG:[00:07:01 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[00:07:32 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[00:09:14 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[00:11:52 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[00:12:12 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:33:05 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:39:37 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:40:37 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:42:35 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:43:08 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:45:14 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[17:39:20 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[17:44:31 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[17:53:57 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:23:35 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:32:13 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:34:24 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:38:10 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:40:29 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:40:54 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michael
suite run_rapid #  begun:1 state:complete flag:message
edit ECF_INCLUDE '/home/michael/host_share/rapid_run/ecflow'
edit ECF_FILES '/home/michael/host_share/rapid_run/ecflow/run_rapid'
edit ECF_HOME '/home/michael/host_share/rapid_run/ecflow'
calendar initTime:2019-Feb-21 18:40:54 suiteTime:2019-Feb-21 20:46:00 duration:02:05:06 initLocalTime:2019-Feb-21 18:40:54 lastTime:2019-Feb-21 20:46:00 calendarIncrement:00:01:00
task prep_task # try:1 state:complete
edit PYSCRIPT '/home/michael/host_share/rapid_run/ecflow/iprep_ecf.py'
edit IO_LOCATION '/home/michael/host_share/rapid-io_init'
edit RUNOFF_LOCATION '/home/michael/host_share/ecmwf'
task ens_member # try:1 state:complete
trigger prep_task == complete
edit PYSCRIPT '/home/michael/host_share/rapid_run/ecflow/run_ecflow.py'
endsuite
# enddef
