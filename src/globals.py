import urllib3
import ssl


def init():
    global http
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager(cert_reqs="CERT_NONE", assert_hostname=False)
