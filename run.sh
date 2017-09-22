#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd "$parent_path"

python ./get_scores.py &&
python ./gen_motd.py &&
python3 ./submit_motd.py
