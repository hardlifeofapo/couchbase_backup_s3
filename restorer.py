#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Python simple module that retrieves the latest backup from Amazon S3 and restores it into Couchbase
'''

__author__ = "Pablo Casado (p.casado.arias@gmail.com)"
__credits__ = ["Francis Varga (nerd@crowdpark.com)"]
__license__ = "To de decided"
__version__ = "0.0.1"
__maintainer__ = "Pablo Casado"
__email__ = "p.casado.arias@gmail.com"
__status__ = "Development"


import time, sys, uuid, json, codecs, getopt, datetime
from couchbase import Couchbase
from boto.s3.connection import S3Connection
from boto.s3.key import Key

ACCESS_KEY_ID = 'PUBLIC_KEY'
SECRET_ACCESS_KEY = 'PRIVATE_KEY'
CB_BUCKET_NAME = 'default'
S3_BUCKET_NAME = 'buck_up'
SERVER_NAME = 'your_server_ip_goes_here'
SERVER_PORT = '8091'
USERNAME = 'your_couchbase_user' #couchbase username
PASSWORD = 'your_couchbase_password' #couchbase password


class Restorer(object):
    def __init__(self):
        # connect to a couchbase server and select bucket where docs are stored
        self.conn = S3Connection(ACCESS_KEY_ID, SECRET_ACCESS_KEY)
        self.couchbase = Couchbase("%s:%s" % (SERVER_NAME, SERVER_PORT), username=USERNAME, password=PASSWORD)
        self.cb_bucket = self.couchbase[CB_BUCKET_NAME]
        
        
    def run(self):
        ini = int( time.time() )
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
            contents = json.loads(key.get_contents_as_string())

            print contents

            try:
                # Try to restore a view. I have no idea on how to do this
                design_doc = { "views": json.dumps(contents['views']) }
                #print "design document"
                #print design_doc
                #print ""
                # save a design document
                #self.cb_bucket['_design/testing'] = json.dumps(design_doc)
            except:
                # See http://www.couchbase.com/issues/browse/MB-5302
                del(contents['_id'])
                del(contents['_rev'])
                del(contents['$flags'])
                del(contents['$expiration'])
            
                print "Restoring document: %s"%(str(key.key))

                self.cb_bucket[str(key.key)] = json.dumps(contents)

        fin = int( time.time() )
        total = (fin - ini) #in seconds
        print 'TIME:::%d' % (total)

        
def main():
    restorer = Restorer()
    restorer.run()
    

if __name__ == "__main__":
    main()