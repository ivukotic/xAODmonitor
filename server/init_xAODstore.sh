#!/bin/sh
#
# chkconfig: - 70 40
# description: xAODreceiver startup script
#
xAODstore=/home/ivukotic/xAODmonitor/server/xAODstore.py

# TMPDIR set to SysV IPC ramdrive to avoid include processing failures
TMPDIR=/dev/shm
export TMPDIR

. /etc/rc.d/init.d/functions

RETVAL=0

case "$1" in
   start)
      echo -n "Starting xAODstore: "
      [ -f $xAODstore ] || exit 1

      daemon $xAODstore
      RETVAL=$?
      echo
      [ $RETVAL -eq 0 ] && touch /var/lock/subsys/xaodstore
        ;;

  stop)
      echo -n "Shutting down xAODstore: "
      killproc xAODstore.py
      RETVAL=$?
      echo
      [ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/xaodstore
        ;;

  restart|reload)
        $0 stop
        $0 start
        RETVAL=$?
        ;;
  status)
        status xAODstore.py
        RETVAL=$?
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac

exit $RETVAL
