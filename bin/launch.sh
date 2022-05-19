#!/bin/bash
cd $SNAP/static
$SNAP/bin/npx http-server $SNAP/static -p 8080 --cors