# 4.12.0
defs_state MIGRATE state>:active flag:message state_change:4380 modify_change:24
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
edit ECF_PID '2658' # server
history / MSG:[16:43:08 21.2.2019] --restart :michaelMSG:[16:45:14 21.2.2019] --restart :michaelMSG:[17:39:20 21.2.2019] --restart :michaelMSG:[17:44:31 21.2.2019] --restart :michaelMSG:[17:53:57 21.2.2019] --restart :michaelMSG:[18:23:35 21.2.2019] --restart :michaelMSG:[18:32:13 21.2.2019] --restart :michaelMSG:[18:34:24 21.2.2019] --restart :michaelMSG:[18:38:10 21.2.2019] --restart :michaelMSG:[18:40:29 21.2.2019] --restart :michaelMSG:[18:40:54 21.2.2019] --restart :michaelMSG:[20:44:41 21.2.2019] --restart :michaelMSG:[21:12:50 21.2.2019] --restart :michaelMSG:[21:21:28 21.2.2019] --restart :michaelMSG:[22:05:19 21.2.2019] --restart :michaelMSG:[22:24:49 21.2.2019] --restart :michaelMSG:[22:36:42 21.2.2019] --restart :michaelMSG:[22:39:03 21.2.2019] --restart :michaelMSG:[23:23:37 21.2.2019] --restart :michaelMSG:[18:34:44 22.2.2019] --restart :michael
history /run_rapid MSG:[16:39:37 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:40:37 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:42:35 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:43:08 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[16:45:14 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[17:39:20 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[17:44:31 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[17:53:57 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:23:35 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:32:13 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:34:24 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:38:10 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:40:29 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:40:54 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[22:05:19 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[22:24:49 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[22:36:42 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[22:39:03 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[23:23:37 21.2.2019] --replace=/run_rapid run_rapid.def parent  :michaelMSG:[18:34:44 22.2.2019] --replace=/run_rapid run_rapid.def parent  :michael
history /run_rapid/ensemble_family/ens_member_52 MSG:[22:37:04 21.2.2019] --force=queued /run_rapid/ensemble_family/ens_member_52  :michael
suite run_rapid #  begun:1 state:active dur:00:02:16 flag:message
edit ECF_INCLUDE '/home/michael/host_share/rapid_run/ecflow'
edit ECF_FILES '/home/michael/host_share/rapid_run/ecflow/run_rapid'
edit ECF_HOME '/home/michael/host_share/rapid_run/ecflow'
calendar initTime:2019-Feb-22 18:34:44 suiteTime:2019-Feb-22 18:37:00 duration:00:02:16 initLocalTime:2019-Feb-22 18:34:44 lastTime:2019-Feb-22 18:37:00 calendarIncrement:00:01:00
task prep_task # try:1 state:complete
edit PYSCRIPT '/home/michael/host_share/rapid_run/ecflow/iprep_ecf.py'
edit IO_LOCATION '/home/michael/host_share/rapid-io_init'
edit RUNOFF_LOCATION '/home/michael/host_share/ecmwf'
family ensemble_family # state:active dur:00:02:16
trigger prep_task == complete
edit PYSCRIPT '/home/michael/host_share/rapid_run/ecflow/run_ecflow.py'
task ens_member_52 # try:1 state:complete
edit JOB_INDEX '0'
task ens_member_51 # try:1 state:complete
trigger ens_member_52 == complete
edit JOB_INDEX '1'
task ens_member_50 # try:1 state:complete
trigger ens_member_51 == complete
edit JOB_INDEX '2'
task ens_member_49 # try:1 state:complete dur:00:00:16
trigger ens_member_50 == complete
edit JOB_INDEX '3'
task ens_member_48 # try:1 state:complete dur:00:00:16
trigger ens_member_49 == complete
edit JOB_INDEX '4'
task ens_member_47 # try:1 state:complete dur:00:00:16
trigger ens_member_48 == complete
edit JOB_INDEX '5'
task ens_member_46 # try:1 state:complete dur:00:00:16
trigger ens_member_47 == complete
edit JOB_INDEX '6'
task ens_member_45 # try:1 state:complete dur:00:00:16
trigger ens_member_46 == complete
edit JOB_INDEX '7'
task ens_member_44 # try:1 state:complete dur:00:00:16
trigger ens_member_45 == complete
edit JOB_INDEX '8'
task ens_member_43 # try:1 state:complete dur:00:00:16
trigger ens_member_44 == complete
edit JOB_INDEX '9'
task ens_member_42 # try:1 state:complete dur:00:00:16
trigger ens_member_43 == complete
edit JOB_INDEX '10'
task ens_member_41 # try:1 state:complete dur:00:00:16
trigger ens_member_42 == complete
edit JOB_INDEX '11'
task ens_member_40 # try:1 state:complete dur:00:00:16
trigger ens_member_41 == complete
edit JOB_INDEX '12'
task ens_member_39 # try:1 state:complete dur:00:00:16
trigger ens_member_40 == complete
edit JOB_INDEX '13'
task ens_member_38 # try:1 state:complete dur:00:00:16
trigger ens_member_39 == complete
edit JOB_INDEX '14'
task ens_member_37 # try:1 state:complete dur:00:00:16
trigger ens_member_38 == complete
edit JOB_INDEX '15'
task ens_member_36 # try:1 state:complete dur:00:01:16
trigger ens_member_37 == complete
edit JOB_INDEX '16'
task ens_member_35 # try:1 state:complete dur:00:01:16
trigger ens_member_36 == complete
edit JOB_INDEX '17'
task ens_member_34 # try:1 state:complete dur:00:01:16
trigger ens_member_35 == complete
edit JOB_INDEX '18'
task ens_member_33 # try:1 state:complete dur:00:01:16
trigger ens_member_34 == complete
edit JOB_INDEX '19'
task ens_member_32 # try:1 state:complete dur:00:01:16
trigger ens_member_33 == complete
edit JOB_INDEX '20'
task ens_member_31 # try:1 state:complete dur:00:01:16
trigger ens_member_32 == complete
edit JOB_INDEX '21'
task ens_member_30 # try:1 state:complete dur:00:01:16
trigger ens_member_31 == complete
edit JOB_INDEX '22'
task ens_member_29 # try:1 state:complete dur:00:01:16
trigger ens_member_30 == complete
edit JOB_INDEX '23'
task ens_member_28 # try:1 state:complete dur:00:01:16
trigger ens_member_29 == complete
edit JOB_INDEX '24'
task ens_member_27 # try:1 state:complete dur:00:01:16
trigger ens_member_28 == complete
edit JOB_INDEX '25'
task ens_member_26 # try:1 state:complete dur:00:01:16
trigger ens_member_27 == complete
edit JOB_INDEX '26'
task ens_member_25 # try:1 state:complete dur:00:01:16
trigger ens_member_26 == complete
edit JOB_INDEX '27'
task ens_member_24 # try:1 state:complete dur:00:01:16
trigger ens_member_25 == complete
edit JOB_INDEX '28'
task ens_member_23 # try:1 state:complete dur:00:01:16
trigger ens_member_24 == complete
edit JOB_INDEX '29'
task ens_member_22 # try:1 state:complete dur:00:02:16
trigger ens_member_23 == complete
edit JOB_INDEX '30'
task ens_member_21 # try:1 state:complete dur:00:02:16
trigger ens_member_22 == complete
edit JOB_INDEX '31'
task ens_member_20 # try:1 state:complete dur:00:02:16
trigger ens_member_21 == complete
edit JOB_INDEX '32'
task ens_member_19 # try:1 state:complete dur:00:02:16
trigger ens_member_20 == complete
edit JOB_INDEX '33'
task ens_member_18 # try:1 state:complete dur:00:02:16
trigger ens_member_19 == complete
edit JOB_INDEX '34'
task ens_member_17 # try:1 state:complete dur:00:02:16
trigger ens_member_18 == complete
edit JOB_INDEX '35'
task ens_member_16 # try:1 state:complete dur:00:02:16
trigger ens_member_17 == complete
edit JOB_INDEX '36'
task ens_member_15 # passwd:ptCI/yP1 rid:12837 try:1 state:active dur:00:02:16
trigger ens_member_16 == complete
edit JOB_INDEX '37'
task ens_member_14 # state:queued
trigger ens_member_15 == complete
edit JOB_INDEX '38'
task ens_member_13 # state:queued
trigger ens_member_14 == complete
edit JOB_INDEX '39'
task ens_member_12 # state:queued
trigger ens_member_13 == complete
edit JOB_INDEX '40'
task ens_member_11 # state:queued
trigger ens_member_12 == complete
edit JOB_INDEX '41'
task ens_member_10 # state:queued
trigger ens_member_11 == complete
edit JOB_INDEX '42'
task ens_member_9 # state:queued
trigger ens_member_10 == complete
edit JOB_INDEX '43'
task ens_member_8 # state:queued
trigger ens_member_9 == complete
edit JOB_INDEX '44'
task ens_member_7 # state:queued
trigger ens_member_8 == complete
edit JOB_INDEX '45'
task ens_member_6 # state:queued
trigger ens_member_7 == complete
edit JOB_INDEX '46'
task ens_member_5 # state:queued
trigger ens_member_6 == complete
edit JOB_INDEX '47'
task ens_member_4 # state:queued
trigger ens_member_5 == complete
edit JOB_INDEX '48'
task ens_member_3 # state:queued
trigger ens_member_4 == complete
edit JOB_INDEX '49'
task ens_member_2 # state:queued
trigger ens_member_3 == complete
edit JOB_INDEX '50'
task ens_member_1 # state:queued
trigger ens_member_2 == complete
edit JOB_INDEX '51'
endfamily
endsuite
# enddef
