#!/bin/bash
message=$1
echo 🔴 Parameters required: ssh_key_path, repository_ssh_url, commit_message

if [ -z "$1" ]; then
  echo "👿 Please enter required parameters; (SSH key path, repo SSH url and commit message 👿"
  exit 1
fi
if [ -z "$2" ]; then
  echo "👿 Please enter repository SSH url and commit message 👿"
  exit 1
fi
if [ -z "$3" ]; then
  echo "👿 Please enter commit message 👿"
  exit 1
fi
echo COMMIT - 🎽🎽 - add and commit the code

git add .
git commit -m "$3"

echo 🎽🎽🎽🎽 push the code ... using SSH Key ...

eval "$(ssh-agent -s)"
ssh-add $1 && ssh -T git@github.com

echo 🍎 🍎 🍎 SET REMOTE SSH URL ...
git remote set-url origin $2

echo 🍎 🍎 🍎 PUSH, SKOROKORO!!
git push

echo DONE!! 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 

# git@github.com:iqlab-africa/starter-example.git
# ~/.ssh/i_account2