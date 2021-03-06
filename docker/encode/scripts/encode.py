#!/usr/bin/python
import sys
import os
import boto
import boto.s3
import boto.s3.connection

title = sys.argv[1]
if not title:
  raise Exception('Please choose a title')
  sys.exit

#print 'Adding VOB to swift'
#cmd = """swift upload srvbcvideo /mnt/{title}.vob""".format(title=title)
#print cmd
#os.system(cmd)

ripcmd = """cat {title}.vob|avconv -i - -threads 6 \
-s 640x480 -vcodec libx264 -strict experimental -acodec aac -b 512k -ab 128k -ac 1 {title}-1.mp4
qtfaststart {title}-1.mp4 {title}.mp4""".format(title=title)
#flvtool2 -UP {title}.flv
#-b 256k -ab 128k -ac 1 -ar 22050 -aspect 4:4 -s 640x480 -g 30 -qscale 10 -vf "crop=639:479:2:1" {title}.flv
# -acodec libmp3lame  # in flv

print ripcmd
os.system(ripcmd)

# AWS ACCESS DETAILS
AWS_ACCESS_KEY_ID = 'CLBz1dWroWGCBwZvYVuQ'
AWS_SECRET_ACCESS_KEY = 'cpHZEQtGX7iq6UivUdOezUXr4BrikfATwe1zmzeP'

bucket_name = 'srvbcvideo'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        host = 'objects.dreamhost.com',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)
bucket = conn.get_bucket(bucket_name)

uploadfile = title+'.mp4'
print 'Uploading %s to Swift container %s' % \
       (uploadfile, bucket_name)
os.system('swift upload %s %s' % \
       (bucket_name, uploadfile))

print 'Uploading %s to Amazon S3 bucket %s' % \
       (uploadfile, bucket_name)

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

from boto.s3.key import Key
k = Key(bucket)
k.key = uploadfile
k.set_contents_from_filename(uploadfile, cb=percent_cb, num_cb=10)
k.set_canned_acl('public-read')
print 'Done!\n'

