#!/bin/bash

# start up ssh tunnel to ec2 jupiter
ssh -NfL 65432:localhost:65432 magonote

# sshfs mount ec2 vol
sshfs magonote:galvanize-magonote ~/Desktop/ec2-magonote/
 