#
# This code must be compatible with python 2.3
#
import os
import sys
import socket

ZKCLI = os.environ.get('ZKCLI', 'cli_st')
ZKHOST = os.environ.get('ZKHOST', 'localhost:2181')

def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('239.255.0.0', 9))
        return s.getsockname()[0]
    except socket.error:
        sys.exit(1)

def myhostname():
    return socket.gethostname()

def join(service, ip, hostname):
    (cin, cout, cerr) = os.popen3('%s %s' % (ZKCLI, ZKHOST), 'rw')
    cin.write('create /services/%s\n' % (service))
    cin.write('create +e /services/%s/%s\n' % (service, ip))
    cin.write('set /services/%s/%s {"hostname": "%s", "enabled": "1", "nodename": "%s"}\n' % (service, ip, hostname, ip))
    cin.flush()

if __name__ == '__main__':
    ip = myip()
    hostname = myhostname()
    join(sys.argv[1], ip, hostname)
