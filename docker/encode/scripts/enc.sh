#!/bin/bash
BASE=/vagrant/
cd $BASE
FILES=`ls *.vob`

for file in $FILES; do
   TITLE=`basename -s .vob $file`
   exec 2<> $BASE/logs/$TITLE.log
   /root/scripts/encode.py $TITLE
   mv $file $BASE/done/
   rm $BASE/$TITLE-1.mp4
   mv $BASE/$TITLE.mp4 $BASE/done/
done
