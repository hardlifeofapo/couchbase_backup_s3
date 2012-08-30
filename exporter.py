#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Python simple module that retrieves a backup from Amazon S3 and restores it into Couchbase
'''

__author__ = "Pablo Casado (p.casado.arias@gmail.com)"
__credits__ = ["Francis Varga (nerd@crowdpark.com)"]
__license__ = "To de decided"
__version__ = "0.0.2"
__maintainer__ = "Pablo Casado"
__email__ = "p.casado.arias@gmail.com"
__status__ = "Development"


import time, sys, uuid, json, codecs, getopt, datetime, subprocess
import commands
from couchbase import Couchbase
from boto.s3.connection import S3Connection
from boto.s3.key import Key

ACCESS_KEY_ID = 'PUBLIC_KEY'
SECRET_ACCESS_KEY = 'PRIVATE_KEY'
CB_BUCKET_NAME = 'default'
S3_BUCKET_NAME = 'buck_up'
SERVER_NAME = '176.58.119.212'
SERVER_PORT = '8091'


class Exporter(object):
    def __init__(self):
        # connect to a couchbase server and select bucket where docs are stored
        self.conn = S3Connection(ACCESS_KEY_ID, SECRET_ACCESS_KEY)
        now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        self.s3BucketName = "%s_%s_%s" % (ACCESS_KEY_ID.lower(), S3_BUCKET_NAME, now)        
        
    def run(self):
        ini = int( time.time() )
        url = '/usr/bin/curl http://%s:%s/%s/_all_docs?include_docs=true'% (SERVER_NAME, 8092, CB_BUCKET_NAME )
        p = subprocess.Popen(url, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = p.communicate()
        output = json.loads(output)
        items = output['rows']


        # Create does not create again a bucket if that bucket already exists.
        s3_bucket = self.conn.create_bucket(self.s3BucketName) 
        
        for item in items:
            k = Key(s3_bucket)
            k.key = item["doc"]["_id"]
            print "Saving %s" % (item["doc"]["_id"])
            # json.dumps is needed to prevent unicode representation of strings in python, like u'a_string'
            k.set_contents_from_string( json.dumps(item["doc"], sort_keys=True)  )

        fin = int( time.time() )
        total = (fin - ini) #in seconds
        
        print 'TIME:::%d' % (total)

def main():
    exporter = Exporter()
    exporter.run()
    

if __name__ == "__main__":
    main()