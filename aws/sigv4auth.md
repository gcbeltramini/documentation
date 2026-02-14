# Using AWS Signature Version 4 for API requests

This document provides an overview of how to use AWS Signature Version 4 for signing API requests to
AWS services. AWS Signature Version 4 is a protocol for authenticating API requests by adding a
signature to the request headers.

References:

- <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html>
- <https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html>

## Steps to Sign API Requests

1. **Create a Canonical Request**: This involves creating a string that includes the HTTP method,
   canonical URI, canonical query string, canonical headers, and signed headers.
2. **Create a String to Sign**: This string includes the algorithm, request date and time, credential
   scope, and the hashed canonical request.
3. **Calculate the Signature**: Use the AWS secret access key to calculate the signature using the
   HMAC-SHA256 algorithm.
4. **Add the Signature to the Request**: Include the signature in the `Authorization` header of the
   API request.

The Python script `sigv4auth.py` contains two strategies to generate AWS Signature Version 4 (SigV4)
authentication headers for AWS services:

1. Manually construct SigV4-signed requests, by building the canonical request, string to sign, and
   signature, and assembling the required HTTP headers;
2. Use the official `botocore` library.

In addition to these implementation functions, the script also includes example usage code at the
bottom of the file that runs when the script is executed directly. This example uses one of the
strategies to make a request to an AWS service and prints the response, which helps verify that the
generated headers are correct.
