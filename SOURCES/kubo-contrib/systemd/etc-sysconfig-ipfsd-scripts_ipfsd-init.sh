#!/usr/bin/bash

JOURNAL_IDENTIFIER=$1
AUTO_INIT=$2
IPFS_PATH=$3
MOUNTPOINT_IPFS=$4
MOUNTPOINT_IPNS=$5

# Used in ExecStarPre= in the ipfsd.service definition file to check for
# minimally correct conditions and run --init if need by. Messages will land in
# the log files: journalctl -xe -t ipfsd.service

if [[ ! -d $MOUNTPOINT_IPFS ]]
then
  echo "\
ipfsd.service start failure due to unsatisfied pre-conditions. IPFS mountpoint is not a directory or doesn't exist.
  IPFS mountpoint: '$MOUNTPOINT_IPFS'
" | systemd-cat -t $JOURNAL_IDENTIFIER
  exit 1
fi

if [[ ! -d $MOUNTPOINT_IPNS ]]
then
  echo "\
ipfsd.service start failure due to unsatisfied pre-conditions. IPNS mountpoint is not a directory or doesn't exist.
  IPNS mountpoint: '$MOUNTPOINT_IPNS'
" | systemd-cat -t $JOURNAL_IDENTIFIER
  exit 1
fi

if [[ ! -f ${IPFS_PATH}/config ]]
then
  echo "\
...
ipfsd.service start failure due to unsatisfied pre-conditions. May attempt to
auto-initialize. AUTO_INIT=${AUTO_INIT}.

Before running 'systemctl start ipfsd.service' for the very first time, you
have to initialize the service therefore populating its data directory
(repository) located at ${IPFS_PATH}.
...
" | systemd-cat -t $JOURNAL_IDENTIFIER
  if [[ $AUTO_INIT ]]
    echo "Attempting to auto-initialize ${IPFS_PATH}" | systemd-cat -t $JOURNAL_IDENTIFIER
    IPFS_PATH=$IPFS_PATH /usr/bin/ipfs init --empty-repo
  then
    exit 1
  fi
fi


