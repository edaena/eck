import os
import ssl
import sys
import urllib3
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context

urllib3.disable_warnings()
print("Elasticsearch Test")

user="elastic"

get_password_cmd = "kubectl -n elasticsearch get secret quickstart-es-elastic-user -o=jsonpath=\'{.data.elastic}\' | base64 --decode"
password = os.popen(get_password_cmd).read()

print("password " + str(password))

ssl_context = create_ssl_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

es = Elasticsearch(
    ['localhost'],
    http_auth=(user, password),
    scheme="https",
    port=9200,
    verify_certs=False,
    ssl_context=ssl_context,
)

# Create test-index
index = "test-index"
document_id="test-document"
print("Create elasticsearch index " + index)

response=es.indices.create(index=index, ignore=400)

if "status" in response.keys() and response['status']==400:
  print("FAIL: Create elasticsearch index '%s'" % index)
  sys.exit()

assert(response['acknowledged'])

print("Create document '%s' on index '%s'" % (document_id, index))
try:
    document = {"message": "Testing elasticsearch"}
    es.create(index=index, id=document_id, body=document)
    print("Document created on index '%s'" % index)
except:
    print("FAIL: Create document on index '%s'" % index)
    sys.exit()

print("Delete document '%s'" % document_id)
try:
    es.delete(index=index, id=document_id)
except:
    print("FAIL: Delete document '%s' on index '%s'" % (document_id, index))
    sys.exit()

print("Delete index '%s'" % index)
try:
    es.indices.delete(index=index)
except:
    print("FAIL: Delete index '%s'")
    sys.exit()

print("Test Status: PASSED")
