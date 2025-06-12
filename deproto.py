import google_auth_pb2 as pb
import base64
from urllib.parse import urlparse, parse_qs

debug = False

def get_payload_from_otp_url(otp_url: str, i: int, source: str) -> pb.MigrationPayload:
    '''Extracts the otp migration payload from an otp url. This function is the core of the this application.'''
    
    parsed_url = urlparse(otp_url)
    if debug: print(f"parsed_url={parsed_url}")
    try:
        params = parse_qs(parsed_url.query, strict_parsing=True)
    except Exception:  # workaround for PYTHON <= 3.10
        params = {}
    if debug: print(f"querystring params={params}")
    if 'data' not in params:
        print(f"could not parse query parameter in input url\nsource: {source}\nurl: {otp_url}")
        return None
    data_base64 = params['data'][0].replace(' ', '+')
    data = base64.b64decode(data_base64, validate=True)
    payload = pb.MigrationPayload()
    try:
        payload.ParseFromString(data)
    except Exception as e:
        print(f"Cannot decode otpauth-migration migration payload.\n"
              f"data={data_base64}", e)
    if debug: print(f"\n{i}. Payload Line", payload, sep='\n')

    return payload