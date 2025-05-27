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
    parser.add_argument('--output', required=True, help='Output directory to save results')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Read QR code from input file
    decoded_urls = read_qr(args.input)
    
    for url in decoded_urls:
        payload = get_payload_from_otp_url(url, 0, "unknown")
        otps = to_otp(payload)
        otps = fix_issuers(otps)
        save_all_otps(otps, args.output)

if __name__ == "__main__":
    main()