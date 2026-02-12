# Using AWS Signature Version 4 for API requests

This document provides an overview of how to use AWS Signature Version 4 for signing API requests to AWS services. AWS Signature Version 4 is a protocol for authenticating API requests by adding a signature to the request headers.

## Steps to Sign API Requests

1. **Create a Canonical Request**: This involves creating a string that includes the HTTP method, canonical URI, canonical query string, canonical headers, and signed headers.
2. **Create a String to Sign**: This string includes the algorithm, request date and time, credential scope, and the hashed canonical request.
3. **Calculate the Signature**: Use the AWS secret access key to calculate the signature using the HMAC-SHA256 algorithm.
4. **Add the Signature to the Request**: Include the signature in the `Authorization` header of the API request.

## Example Code

Here is an example of how to sign an API request using AWS Signature Version 4 in Python:

```python
import hashlib
import hmac
import datetime


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


# Example usage
access_key = 'YOUR_ACCESS_KEY'
secret_key = 'YOUR_SECRET_KEY'
region = 'us-west-2'
service = 's3'
host = 's3.amazonaws.com'
endpoint = 'https://s3.amazonaws.com'
request_parameters = 'Action=ListBuckets&Version=2006-03-01'

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

# Create the canonical request
canonical_uri = '/'
canonical_querystring = request_parameters
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n'
signed_headers = 'host;x-amz-date'
payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
canonical_request = 'GET' + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

# Create the string to sign
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' + amz_date + '\n' + credential_scope + '\n' + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

# Calculate the signature
signing_key = get_signature_key(secret_key, date_stamp, region, service)
signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

# Add the signature to the request
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
# Now you can use the `authorization_header` in your API request headers
```

## Conclusion

Using AWS Signature Version 4 ensures that your API requests are securely authenticated. It is important to follow the steps outlined above to correctly sign your requests and avoid authentication errors. Always keep your AWS access keys secure and do not share them publicly.
