import os
import re
from qrcode import QRCode

def save_all_otps(otps: list[dict], dir: str) -> None:
    for j, otp in enumerate(otps):
        save_qr_image(otp, dir, j)

def save_qr_image(otp: dict, dir: str, j: int) -> str:
    if not (os.path.exists(dir)): os.makedirs(dir, exist_ok=True)
    pattern = re.compile(r'[\W_]+')
    file_otp_name = pattern.sub('', otp['name'])
    file_otp_issuer = pattern.sub('', otp['issuer'])
    save_qr_image_file(otp['url'], f"{dir}/{j}-{file_otp_name}{'-' + file_otp_issuer if file_otp_issuer else ''}.png")
    return file_otp_name


def save_qr_image_file(otp_url: str, name: str) -> None:
    qr = QRCode()
    qr.add_data(otp_url)
    img = qr.make_image(fill_color='black', back_color='white')
    print(f"Saving to {name}")
    img.save(name)  # type: ignore