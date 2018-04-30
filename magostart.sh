#!/bin/bash

# start up ssh tunnel to ec2 jupiter
ssh -NfL 65432:localhost:65432 magonote

# sshfs mount ec2 vol
sshfs magonote:galvanize-magonote ~/Desktop/ec2-magonote/

# status of downloads
echo "files in html/post_pages:"
ssh magonote "ls -1 galvanize-magonote/html/post_pages | wc -l"
echo "files under 2000 bytes:"
ssh magonote "find galvanize-magonote/html/post_pages -size -2000c"

