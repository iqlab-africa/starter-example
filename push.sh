#!/bin/bash
message=$1

if [ -z "$1" ]; then
  echo "👿 Please enter commit message 👿"
  exit 1
fi
echo COMMIT - 🎽🎽 - add and commit the code

git add .
git commit -m "$1"

echo 🎽🎽🎽🎽 push the code ... using SSH Key ...

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/i_account2 && ssh -T git@github.com

echo 🍎 🍎 🍎 SET REMOTE SSH URL ...
git remote set-url origin git@github.com:iqlab-africa/starter-example.git

echo 🍎 🍎 🍎 PUSH, SKOROKORO!!
git push

echo DONE!! 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 