from read import read_qr
import argparse
import os
from deproto import get_payload_from_otp_url
from to_otp import to_otp
from issuer_dict import fix_issuers
from write import save_all_otps

def main():
    parser = argparse.ArgumentParser(description='Read QR codes from an image file')
    parser.add_argument('--input', required=True, help='Input image file containing QR code')
    parser.add_argument('--output', required=False, help='Output directory to save results')
    parser.add_argument('--print', action='store_true', help='Print OTPs to console')
    
    args = parser.parse_args()

    if not args.output and not args.print:
        print("Please provide either --output or --print")
        return
    
    # Read QR code from input file
    decoded_urls = read_qr(args.input)
    
    for url in decoded_urls:
        payload = get_payload_from_otp_url(url, 0, "unknown")
        otps = to_otp(payload)
        otps = fix_issuers(otps)
        if args.output:
            os.makedirs(args.output, exist_ok=True)
            save_all_otps(otps, args.output)
        if args.print:
            for otp in otps:
                print(f"{otp['issuer']} {otp['name']}: {otp['url']}")

if __name__ == "__main__":
    main()