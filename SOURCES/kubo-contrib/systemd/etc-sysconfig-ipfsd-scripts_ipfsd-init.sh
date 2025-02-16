#!/usr/bin/bash

AUTO_INIT=$2
IPFS_PATH=$3
MOUNTPOINT_IPFS=$4
MOUNTPOINT_IPNS=$5

# Used in ExecStarPre= in the ipfsd.service definition file to check for
# minimally correct conditions and run --init if need by. Messages will land in
# the systemd Journal of the Unit: journalctl -eu ipfsd.service

if [[ ! -d $MOUNTPOINT_IPFS ]]
then
  echo "\
ipfsd.service start failure due to unsatisfied pre-conditions. IPFS mountpoint is not a directory or doesn't exist.
  IPFS mountpoint: '$MOUNTPOINT_IPFS'
"
  exit 1
fi

if [[ ! -d $MOUNTPOINT_IPNS ]]
then
  echo "\
ipfsd.service start failure due to unsatisfied pre-conditions. IPNS mountpoint is not a directory or doesn't exist.
  IPNS mountpoint: '$MOUNTPOINT_IPNS'
"
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
"
  if [[ $AUTO_INIT ]]
    echo "Attempting to auto-initialize ${IPFS_PATH}"
    IPFS_PATH=$IPFS_PATH /usr/bin/ipfs init --empty-repo
  then
    exit 1
  fi
fi
