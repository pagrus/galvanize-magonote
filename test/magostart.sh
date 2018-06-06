#!/bin/bash

# start up jupyter on remote machine with
# jupyter notebook --no-browser --ip=0.0.0.0 --port=65432 --NotebookApp.token=''
# for reference this will start jupyter in your home dir
# jupyter notebook --notebook-dir=/home/username
# default home dir on aws ubuntu install
# /home/ubuntu/galvanize-magonote/

# start up ssh tunnel to ec2 jupiter
ssh -NfL 65432:localhost:65432 magonote
# note: if you need to find (& reset?) your tunnel you can find it with 
# ps aux | grep 65432
# and then kill <pid> for example. you don't need a -9 or anything

# connect to local tunnel endpoint using browser:
# http://localhost:65432

# sshfs mount ec2 vol
sshfs magonote:galvanize-magonote ~/Desktop/ec2-magonote/

# status of downloads
echo "files in html/post_pages:"
ssh magonote "ls -1 galvanize-magonote/html/post_pages | wc -l"
echo "files under 2000 bytes:"
ssh magonote "find galvanize-magonote/html/post_pages -size -2000c"
