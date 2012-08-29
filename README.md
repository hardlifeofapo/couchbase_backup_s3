couchbase_backup_s3
===================

Python simple module that exports documents from Couchbase and imports them into Amazon S3 

Requires:

a) boto (easy_install boto should be enough)

b) Amazon Web Services Auth Keys. You can get them here:

	https://portal.aws.amazon.com/gp/aws/securityCredentials

c) Creating a couchbase view that can return all the documents, like this:

    function (doc) {
        emit(doc._id, null);
    }

By default, the view is named "_design/all/_view/all".

You can change it by specifying the value of constant ALL_DOCS_VIEW_NAME. It will be called with __include_docs=true__