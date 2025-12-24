#!/usr/bin/env bash
eval $(keychain --eval --agents ssh -Q --quiet $HOME/.ssh/dvoosteroom)
ssh -4 -i $HOME/.ssh/dvoosteroom dvoosteroom@snellius.surf.nl
