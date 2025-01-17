import socket
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def get_serial(host, port):
    try:
        # Create an SSL context that doesn't verify certificates
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Create a socket connection and fetch the certificate
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                # Retrieve the raw DER-encoded certificate
                der_cert = ssock.getpeercert(binary_form=True)

        # Parse the certificate using cryptography
        cert = x509.load_der_x509_certificate(der_cert, default_backend())

        # Extract the commonName (CN) from the subject
        for attribute in cert.subject:
            if attribute.oid == x509.NameOID.COMMON_NAME:
                return attribute.value

        print("commonName not found in certificate.")
        return None
    except Exception as e:
        print(f"Failed to retrieve certificate: {e}")
        return None
    

