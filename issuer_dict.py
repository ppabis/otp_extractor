import google_auth_pb2 as pb

ISSUERS = {
    'Amazon Web Services': 'AWS',
    'gitlab.com': 'GitLab',
    'gandi.net': 'Gandi',
}

def get_issuer(issuer: str) -> str:
    return ISSUERS.get(issuer, issuer)

def fix_issuers(otps: list[dict]) -> list[dict]:
    for otp in otps:
        otp['issuer'] = get_issuer(otp['issuer'])
    return otps

def fix_proto_issuer(otp: pb.MigrationPayload.OtpParameters) -> pb.MigrationPayload.OtpParameters:
    otp.issuer = get_issuer(otp.issuer)
    return otp