import base64,json,os,pathlib,sys,tempfile
sys.path.insert(0,str(pathlib.Path(__file__).parents[1]/"memory"))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import receipt_auth
private=Ed25519PrivateKey.generate()
raw=private.private_bytes(serialization.Encoding.Raw,serialization.PrivateFormat.Raw,serialization.NoEncryption())
pub=private.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
os.environ["HELO_RECEIPT_ED25519_PUBLIC_KEYS_JSON"]=json.dumps({"k1":base64.b64encode(pub).decode()})
signed=receipt_auth.sign_ed25519({"op_id":"helo-test","status":"COMPLETED"},base64.b64encode(raw).decode(),"k1")
receipt_auth.verify(signed)
signed["status"]="FAILED"
try:
    receipt_auth.verify(signed);raise AssertionError("tampered Ed25519 receipt accepted")
except ValueError as e: assert str(e)=="RECEIPT_AUTHENTICATION_FAILED"
os.environ["HELO_RECEIPT_HMAC_KEYS_JSON"]=json.dumps({"old":"11"*32,"new":"22"*32})
r={"op_id":"rotation","signature_algorithm":"hmac-sha256","signing_key_id":"new"}
import hashlib,hmac
r["receipt_hmac_sha256"]=hmac.new(bytes.fromhex("22"*32),receipt_auth.canonical(r,{"receipt_hmac_sha256"}),hashlib.sha256).hexdigest()
receipt_auth.verify(r)
print("PASS Ed25519 separation, tamper rejection, and HMAC key rotation")
