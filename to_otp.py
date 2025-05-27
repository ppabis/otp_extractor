import google_auth_pb2 as pb
import base64
from urllib.parse import urlparse, quote, urlencode
from issuer_dict import fix_proto_issuer

def convert_secret_from_bytes_to_base32_str(bytes: bytes) -> str:
    return str(base64.b32encode(bytes), 'utf-8').replace('=', '')

def get_enum_name_by_number(parent, field_name: str) -> str:
    field_value = getattr(parent, field_name)
    return parent.DESCRIPTOR.fields_by_name[field_name].enum_type.values_by_number.get(field_value).name  # type: ignore # generic code

def get_otp_type_str_from_code(otp_type: int) -> str:
    return 'totp' if otp_type == 2 else 'hotp'

def build_otp_url(secret: str, raw_otp: pb.MigrationPayload.OtpParameters) -> str:
    url_params = {'secret': secret}
    if raw_otp.type == 1: url_params['counter'] = str(raw_otp.counter)
    if raw_otp.issuer: url_params['issuer'] = raw_otp.issuer
    otp_url = f"otpauth://{get_otp_type_str_from_code(raw_otp.type)}/{quote(raw_otp.name)}?" + urlencode(url_params)
    return otp_url

def to_otp(payload: pb.MigrationPayload):
    otps = []
    for raw_otp in payload.otp_parameters:
        secret = convert_secret_from_bytes_to_base32_str(raw_otp.secret)
        print('OTP enum type:', get_enum_name_by_number(raw_otp, 'type'))
        otp_type = get_otp_type_str_from_code(raw_otp.type)
        raw_otp = fix_proto_issuer(raw_otp)
        otp_url = build_otp_url(secret, raw_otp)
        otp = {
            "name": raw_otp.name,
            "secret": secret,
            "issuer": raw_otp.issuer,
            "type": otp_type,
            "counter": raw_otp.counter if raw_otp.type == 1 else None,
            "url": otp_url
        }
        otps.append(otp)
    return otps