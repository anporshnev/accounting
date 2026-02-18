import hashlib

def get_hash(args):
    hash = hashlib.sha256()
    bytes = "".join(args).encode()
    hash.update(bytes)
    return hash.hexdigest()