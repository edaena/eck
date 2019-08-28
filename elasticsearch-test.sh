#! /usr/bin/env bash


ELASTICSEARCH_PASSWORD="$(kubectl -n elasticsearch get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)"


echo "Create index: testindex"
response="$(curl -X PUT -u "elastic:${ELASTICSEARCH_PASSWORD}" -k "https://localhost:9200/testindex")"
echo $response

echo "Check index testindex exists"
response="$(curl -X GET -u "elastic:${ELASTICSEARCH_PASSWORD}" -k "https://localhost:9200/testindex")"
echo $response


echo "Create document: testdocument"
response="$(curl -X PUT -u "elastic:${ELASTICSEARCH_PASSWORD}" -k "https://localhost:9200/testindex/_create/testdoc" -H 'Content-Type: application/json' -d'{"user" : "testuser","post_date" : "2009-11-15T14:12:12","message" : "Elasticsearch test"}')"

echo "Check document testdoc exists"
response="$(curl -X GET -u "elastic:${ELASTICSEARCH_PASSWORD}" -k "https://localhost:9200/testindex/_doc/testdoc")"


echo "Delete testdoc"
response="$(curl -X DELETE -u "elastic:${ELASTICSEARCH_PASSWORD}" -k "https://localhost:9200/testindex/_doc/testdoc")"

echo "Delete testindex"
response="$(curl -X DELETE -u "elastic:${ELASTICSEARCH_PASSWORD}" -k "https://localhost:9200/testindex")"
echo $response

# Verify Index deleted

# '{"acknowledged":true}'
