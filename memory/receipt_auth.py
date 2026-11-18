import base64,hashlib,hmac,json,os
def canonical(receipt, excluded):
    return json.dumps({k:v for k,v in receipt.items() if k not in excluded},sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def _hmac_keys():
    raw=os.environ.get("HELO_RECEIPT_HMAC_KEYS_JSON","")
    if raw:
        data=json.loads(raw);return {str(k):bytes.fromhex(v) for k,v in data.items()}
    legacy=os.environ.get("HELO_RECEIPT_HMAC_KEY_HEX","")
    return {"legacy":bytes.fromhex(legacy)} if legacy else {}
def verify(receipt):
    alg=receipt.get("signature_algorithm","hmac-sha256")
    key_id=str(receipt.get("signing_key_id","legacy"))
    if alg=="ed25519":
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        keys=json.loads(os.environ.get("HELO_RECEIPT_ED25519_PUBLIC_KEYS_JSON","{}"))
        if key_id not in keys: raise ValueError("RECEIPT_SIGNING_KEY_UNKNOWN")
        try:
            pub=Ed25519PublicKey.from_public_bytes(base64.b64decode(keys[key_id],validate=True))
            sig=base64.b64decode(receipt.get("receipt_signature",""),validate=True)
            pub.verify(sig,canonical(receipt,{"receipt_signature"}))
        except Exception as e:
            if str(e)=="RECEIPT_SIGNING_KEY_UNKNOWN": raise
            raise ValueError("RECEIPT_AUTHENTICATION_FAILED")
        return
    if alg!="hmac-sha256": raise ValueError("RECEIPT_SIGNATURE_ALGORITHM_UNSUPPORTED")
    keys=_hmac_keys()
    if key_id not in keys or len(keys[key_id])<32: raise ValueError("RECEIPT_AUTH_KEY_REQUIRED")
    supplied=receipt.get("receipt_hmac_sha256","")
    expected=hmac.new(keys[key_id],canonical(receipt,{"receipt_hmac_sha256"}),hashlib.sha256).hexdigest()
    if not isinstance(supplied,str) or not hmac.compare_digest(supplied,expected): raise ValueError("RECEIPT_AUTHENTICATION_FAILED")
def sign_ed25519(receipt,private_key_b64,key_id):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    out=dict(receipt);out["signature_algorithm"]="ed25519";out["signing_key_id"]=key_id
    key=Ed25519PrivateKey.from_private_bytes(base64.b64decode(private_key_b64,validate=True))
    out["receipt_signature"]=base64.b64encode(key.sign(canonical(out,{"receipt_signature"}))).decode()
    return out
