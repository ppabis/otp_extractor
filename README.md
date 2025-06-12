Google Authenticator Export -> OTP converter
======================

This project is based on:
[https://github.com/scito/extract_otp_secrets](https://github.com/scito/extract_otp_secrets)
and contains plenty of copy-paste from that project. I just wanted a simpler
version that will load screenshots.

From screenshots of Google Authenticator exports this application will create
fresh QR codes and print `otpauth://` addresses to the console.

Install requirements with `venv` and optionally compile the Protobuf model file.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. google_auth.proto
```

### Usage

```bash
python main.py --input myexport.jpg --output new_qr_codes --print
```

### Parameters

* `--input` - specify input image with export from Authenticator to process,
* `--output` - save all OTP QR codes into this directory (optional),
* `--print` - print `otpauth://` addresses of all OTPs.

Either `output` or `print` must be specified.

In `issuer_dict.py` you can also override issuers that are too long. For example
`Amazon Web Services` takes almost entire screen and can't be changes in Google
Authenticator. I prefer to replace it with `AWS`. Add your own to the list if
you need.
