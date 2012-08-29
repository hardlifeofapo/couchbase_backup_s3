#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Python simple module that retrieves the latest backup from Amazon S3 and restores it into Couchbase
'''

__author__ = "Pablo Casado (p.casado.arias@gmail.com)"
__credits__ = []
__license__ = "To de decided"
__version__ = "0.0.1"
__maintainer__ = "Pablo Casado"
__email__ = "p.casado.arias@gmail.com"
__status__ = "Development"


import time, sys, uuid, json, codecs, getopt, datetime
from couchbase import Couchbase
from boto.s3.connection import S3Connection
from boto.s3.key import Key

ACCESS_KEY_ID = 'YOUR_PUBLIC_KEY_HERE'
SECRET_ACCESS_KEY = 'YOUR_PRIVATE_KEY_HERE'
CB_BUCKET_NAME = 'default'
S3_BUCKET_NAME = 'buck_up'
SERVER_NAME = 'your_ip_goes_here'
SERVER_PORT = '8091'
ALL_DOCS_VIEW_NAME = '_design/all/_view/all'
USERNAME = 'your_username' #couchbase username
PASSWORD = 'your_password' #couchbase password


class Restorer(object):
    def __init__(self):
        # connect to a couchbase server and select bucket where docs are stored
        self.conn = S3Connection(ACCESS_KEY_ID, SECRET_ACCESS_KEY)
        
        #self.couchbase = Couchbase("%s:%s" % (SERVER_NAME, SERVER_PORT), username=USERNAME, password=PASSWORD)
        #self.cb_bucket = self.couchbase[CB_BUCKET_NAME]
        
        
    def run(self):
        buckets = self.conn.get_all_buckets()
        bucketList = []
        
        for bucket in buckets:
            if bucket.name.startswith(ACCESS_KEY_ID.lower()):
                bucketList.append(bucket.name)
                
        self.s3BucketName = bucketList.pop() # Bucket results are orderer lexicographically, which is good here
        s3_bucket = self.conn.create_bucket(self.s3BucketName) 

        rs = s3_bucket.list()
        for key in rs:
           key = s3_bucket.get_key(key.name)
           contents = key.get_contents_as_string()
           #self.cb_bucket[key.name] = contents

        '''
        ini = int( time.time() )
        items = self.cb_bucket.view(ALL_DOCS_VIEW_NAME, include_docs="true" )

        # Create does not create again a bucket if that bucket already exists.
        s3_bucket = self.conn.create_bucket(self.s3BucketName) 
        
        for item in items:
            k = Key(s3_bucket)
            k.key = item["doc"]["_id"]
            print json.dumps(item["doc"], sort_keys=True) 
            k.set_contents_from_string( json.dumps(item["doc"], sort_keys=True)  )
        
        fin = int( time.time() )
        total = (fin - ini) #in seconds
        
        print 'TIME:::%d' % (total)
        '''
        
def main():
    restorer = Restorer()
    restorer.run()
    

if __name__ == "__main__":
    main()