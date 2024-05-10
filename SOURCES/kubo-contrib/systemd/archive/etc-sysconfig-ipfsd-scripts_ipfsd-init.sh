#!/usr/bin/bash

JOURNAL_IDENTIFIER=$1
AUTO_INIT=$2
REPO=$3
MOUNTPOINT_IPFS=$4
MOUNTPOINT_IPFN=$5

    /usr/bin/echo "$MESSAGE" | systemd-cat -t $JOURNAL_IDENTIFIER

# Used in ExecStarPre= in the ipfsd.service definition file to check for
# minimally correct conditions and run --init if need by. Messages will land in
# the log files: journalctl -xe -t ipfsd.service

if [[ ! -d $MOUNTPOINT_IPFS ]] || [[ ! -d $MOUNTPOINT_IPFN ]]
then
  echo "\
ipfsd.service start failure due to unsatisfied pre-conditions. One or both of these mountpoints is not a directory or doesn't exist:
  $MOUNTPOINT_IPFS
  $MOUNTPOINT_IPFN
" | systemd-cat -t $JOURNAL_IDENTIFIER
  exit 1
fi

if [[ ! -f ${REPO}/config ]]
then
  echo "\
...
ipfsd.service start failure due to unsatisfied pre-conditions. May attempt to
auto-initialize. AUTO_INIT=${AUTO_INIT}.

Before running 'systemctl start ipfsd.service' for the very first time, you
have to initialize the service therefore populating its data directory
(repository) located at ${REPO}.
...
" | systemd-cat -t $JOURNAL_IDENTIFIER
  if [[ $AUTO_INIT ]]
    echo "Attempting to auto-initialize ${REPO}" | systemd-cat -t $JOURNAL_IDENTIFIER
    IPFS_PATH=$REPO /usr/bin/ipfs init --empty-repo
  then
    exit 1
  fi
fi


