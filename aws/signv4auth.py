import hmac
from collections import namedtuple
from datetime import UTC, datetime
from hashlib import sha256
from urllib.parse import urlencode

from botocore.auth import S3SigV4Auth, SigV4Auth
from botocore.awsrequest import AWSRequest
from requests import request


def sign(key: bytes, msg: str, hex: bool = False) -> bytes | str:
    r"""
    Return the HMAC-SHA256 signature for a given message using the provided key.

    Parameters
    ----------
    key : bytes
        The signing key.
    msg : str
        The message to sign.
    hex : bool, optional
        If True, return the signature as a hexadecimal string instead of bytes.

    Returns
    -------
    bytes or str
        The resulting HMAC-SHA256 signature.

    References
    ----------
    - https://github.com/boto/botocore/blob/1efd7be5a454fe5fa8d2b05d7e6d4873c92ebc01/botocore/auth.py#L228-L233

    Examples
    --------
    >>> sign(key=b"my_secret_key", msg="Hello, World!")
    b"\xf3\xca\xf5\xd4~<\x8c\xde\xa3\xb3\xae\x8c\x87\xb6M$}M\xac\xf7\x83\xb8\xd1q\x086y\xd52\x91Y\xcc"
    >>> sign(key=b"my_secret_key", msg="Hello, World!", hex=True)
    "f3caf5d47e3c8cdea3b3ae8c87b64d247d4dacf783b8d171083679d5329159cc"
    """
    hm = hmac.new(key, msg.encode("utf-8"), sha256)
    if hex:
        return hm.hexdigest()
    else:
        return hm.digest()


def get_signature_key(
    aws_secret_access_key: str,
    date_stamp: str,
    aws_region_name: str,
    aws_service_name: str,
) -> bytes:
    r"""
    Derive the AWS Signature Version 4 signing key using the secret access key, date, region, and
    service name.

    Parameters
    ----------
    aws_secret_access_key : str
        AWS secret access key.
    date_stamp : str
        Date in YYYYMMDD format.
    aws_region_name : str
        AWS region name (e.g., "us-west-2").
    aws_service_name : str
        AWS service name (e.g., "s3").

    Returns
    -------
    bytes
        The derived signing key as bytes.

    References
    ----------
    - https://github.com/boto/botocore/blob/1efd7be5a454fe5fa8d2b05d7e6d4873c92ebc01/botocore/auth.py#L410-L418

    Examples
    --------
    >>> get_signature_key(
    ...     aws_secret_access_key="my_secret_key",
    ...     date_stamp="20240601",
    ...     aws_region_name="us-west-2",
    ...     aws_service_name="s3",
    ... )
    b"\xcbqY\xb7\xadv\x10i\xd8\\8.\xad\xde\xf7\xc9^\xdbC\xa9\xd6\xab\xce\x1d\x1dY0\xa9\xd1\x94=@"
    """
    date_key: bytes = sign(("AWS4" + aws_secret_access_key).encode("utf-8"), date_stamp)
    date_region_key: bytes = sign(date_key, aws_region_name)
    date_region_service_key: bytes = sign(date_region_key, aws_service_name)
    signing_key: bytes = sign(date_region_service_key, "aws4_request")
    return signing_key


def generate_aws_headers(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: str | None,
    aws_region: str,
    aws_service: str,
    method: str,
    aws_host: str,
    aws_request_parameters: str | dict[str, str],
    aws_payload: str = "",
) -> dict[str, str]:
    """
    Generate AWS Signature Version 4 headers for authenticating API requests.

    This function constructs the canonical request, string to sign, and signature according to the
    AWS Signature Version 4 process. It returns the required headers to authenticate an AWS API
    request, including the Authorization header.

    Parameters
    ----------
    aws_access_key_id : str
        AWS access key ID.
    aws_secret_access_key : str
        AWS secret access key.
    aws_session_token : str or None
        AWS session token (for temporary credentials; can be empty if not used).
    aws_region : str
        AWS region (e.g., "us-west-2").
    aws_service : str
        AWS service name (e.g., "s3").
    method : str
        HTTP method (e.g., "GET", "POST").
    aws_host : str
        Hostname of the AWS service (e.g., "s3.amazonaws.com").
    aws_request_parameters : str or dict[str, str]
        Query parameters for the request (e.g., "Action=ListBuckets&Version=2006-03-01" or
        {"Action": "ListBuckets", "Version": "2006-03-01"}). If a string is provided, it will be
        used directly, so it must be properly formatted and sorted by query parameter; if a dictionary
        is provided, it will be URL-encoded.
    aws_payload : str, optional
        Request payload (body) as a string.

    Returns
    -------
    dict[str, str]
        Dictionary of headers to include in the AWS API request.

    References
    ----------
    - https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html

    Examples
    --------
    >>> generate_aws_headers(
    ...     aws_access_key_id="AKIA...",
    ...     aws_secret_access_key="SECRET...",
    ...     aws_session_token="SESSION...",
    ...     aws_region="us-west-2",
    ...     aws_service="s3",
    ...     aws_host="s3.amazonaws.com",
    ...     aws_request_parameters="Action=ListBuckets&Version=2006-03-01",
    ...     aws_payload="",
    ...     method="GET",
    ... )
    {"X-Amz-Date": ..., "X-Amz-Security-Token": ..., "Authorization": ...}
    """
    # Create a date for headers and the credential string
    t: datetime = datetime.now(UTC)
    amz_date: str = t.strftime("%Y%m%dT%H%M%SZ")
    date_stamp: str = amz_date[0:8]  # Date without time, used in credential scope

    # 1. Create the canonical request
    canonical_uri: str = "/"
    canonical_query_string: str = (
        aws_request_parameters
        if isinstance(aws_request_parameters, str)
        else urlencode(sorted(aws_request_parameters.items()))
    )
    canonical_headers_dict: dict[str, str] = {
        "host": aws_host,
        "x-amz-date": amz_date,
    }
    if aws_session_token:
        canonical_headers_dict["x-amz-security-token"] = aws_session_token
    canonical_headers: str = "".join(f"{k.lower()}:{v.strip()}\n" for k, v in sorted(canonical_headers_dict.items()))
    signed_headers: str = ";".join(k.lower() for k in sorted(canonical_headers_dict.keys()))
    payload_hash: str = sha256(aws_payload.encode("utf-8")).hexdigest()
    canonical_request: str = (
        method
        + "\n"
        + canonical_uri
        + "\n"
        + canonical_query_string
        + "\n"
        + canonical_headers
        + "\n"
        + signed_headers
        + "\n"
        + payload_hash
    )

    # 2. Create the string to sign
    algorithm: str = "AWS4-HMAC-SHA256"
    credential_scope: str = date_stamp + "/" + aws_region + "/" + aws_service + "/" + "aws4_request"
    string_to_sign: str = (
        algorithm
        + "\n"
        + amz_date
        + "\n"
        + credential_scope
        + "\n"
        + sha256(canonical_request.encode("utf-8")).hexdigest()
    )

    # 3. Calculate the signature
    signing_key: bytes = get_signature_key(aws_secret_access_key, date_stamp, aws_region, aws_service)
    signature: str = hmac.new(signing_key, string_to_sign.encode("utf-8"), sha256).hexdigest()

    # 4. Add the signature to the request
    authorization_header: str = (
        algorithm
        + " "
        + "Credential="
        + aws_access_key_id
        + "/"
        + credential_scope
        + ", "
        + "SignedHeaders="
        + signed_headers
        + ", "
        + "Signature="
        + signature
    )

    headers: dict[str, str] = {
        "X-Amz-Date": amz_date,
        "Authorization": authorization_header,
    }
    if aws_session_token:
        headers["X-Amz-Security-Token"] = aws_session_token
    if aws_service == "s3":
        headers["X-Amz-Content-SHA256"] = payload_hash
        # https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-create-signed-request.html

    return headers


def generate_aws_headers_botocore(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: str | None,
    aws_region: str,
    aws_service: str,
    method: str,
    aws_host: str,
    aws_request_parameters: str | dict[str, str],
) -> dict[str, str]:
    query_parameters: str = (
        aws_request_parameters
        if isinstance(aws_request_parameters, str)
        else urlencode(sorted(aws_request_parameters.items()))
    )
    url: str = "https://" + aws_host.rstrip("/") + "/?" + query_parameters
    aws_request = AWSRequest(method=method, url=url)
    # aws_request = AWSRequest(method="POST", url=url, data=body)
    credentials = namedtuple("Credentials", ["access_key", "secret_key", "token"])  # noqa: PYI024
    credentials = credentials(
        access_key=aws_access_key_id,
        secret_key=aws_secret_access_key,
        token=aws_session_token,
    )
    if aws_service == "s3":
        S3SigV4Auth(credentials, aws_service, aws_region).add_auth(aws_request)
    else:
        SigV4Auth(credentials, aws_service, aws_region).add_auth(aws_request)
    prepared = aws_request.prepare()
    headers = dict(prepared.headers)
    return headers


# Example usage

# Credentials:
aws_access_key_id: str = "A..."
aws_secret_access_key: str = "b..."
aws_session_token: str = "c..."

# Example 1: S3 ListBuckets
method: str = "GET"
aws_region: str = "us-east-1"
# For the global S3 endpoint "s3.amazonaws.com", the signing region must be "us-east-1",
# otherwise this error will be returned:
#   AuthorizationHeaderMalformed: The authorization header is malformed; the region '...' is wrong; expecting 'us-east-1'
# When using regional S3 endpoints (for example, "s3.us-west-2.amazonaws.com"), use the actual region (e.g., "us-west-2").
aws_service: str = "s3"
aws_host: str = "s3.amazonaws.com"
aws_request_parameters: dict[str, str] = {"Action": "ListBuckets", "Version": "2006-03-01"}

# Example 2: STS GetCallerIdentity
method: str = "GET"
aws_region: str = "us-west-2"
aws_service: str = "sts"
aws_host: str = f"sts.{aws_region:s}.amazonaws.com"
aws_request_parameters: dict[str, str] = {"Action": "GetCallerIdentity", "Version": "2011-06-15"}

# Generate headers (also works with `generate_aws_headers_botocore`)
headers: dict[str, str] = generate_aws_headers(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    aws_region=aws_region,
    aws_service=aws_service,
    method=method,
    aws_host=aws_host,
    aws_request_parameters=aws_request_parameters,
)

# Make the request with the generated headers
resp = request(method=method, url=f"https://{aws_host:s}", params=aws_request_parameters, headers=headers)
print(f"Status code: {resp.status_code}")
print(f"Response: {resp.text}")
