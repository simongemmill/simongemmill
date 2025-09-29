#!/bin/bash

# Define credentials
HOST="ssh.ch3y9v6hp.service.one"
USER="ch3y9v6hp_ssh"
PORT=22
LOCAL_DIR="./dashboard"
REMOTE_DIR="/www/dashboard"

# Run SFTP batch
sftp -P $PORT $USER@$HOST <<EOF
cd $REMOTE_DIR
put $LOCAL_DIR/index.html
put $LOCAL_DIR/style.css
put $LOCAL_DIR/script.js
bye
EOF