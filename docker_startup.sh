#!/bin/bash

# this script runs inside the docker container
# it's purpose is to run admin_patches on the server directories

if [[ ! -z "$PATCHES_TARGET_DIR" ]]
then
	cd /magicked_admin_patches
	for i in $(echo $PATCHES_TARGET_DIR | sed "s/,/ /g")
	do
		echo "*** Applying admin_patches to $i ***"
	    echo $'\n'
	    python ./admin_patches.py -t "$i"
	    echo $'\n\n'
	done
	echo $'*** Done applying admin_patches ***\n'
fi

cd /magicked_admin
python /magicked_admin/magicked_admin.py -s