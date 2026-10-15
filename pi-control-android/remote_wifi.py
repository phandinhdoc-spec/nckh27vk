"""DietPi WiFi DB adapter. JSON over SSH stdin; no password in argv or responses.

Supports the native five-slot WPA-PSK/NONE format of dietpi-wifidb. Refuses
custom/EAP configurations rather than letting the native generator erase them.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import tempfile

FIELDS = ('SSID', 'KEY', 'KEYMGR', 'PROTO', 'PAIRWISE', 'AUTH_ALG', 'EAP',
          'IDENTITY', 'PASSWORD', 'PHASE1', 'PHASE2', 'CERT')
SLOTS = 5


def empty_slot():
    return {k: 'WPA-PSK' if k == 'KEYMGR' else '' for k in FIELDS}


def validate_ssid(ssid):
    if (not isinstance(ssid, str) or not 1 <= len(ssid.encode('utf-8')) <= 32
            or any(not c.isprintable() or c in '\\"' for c in ssid)):
        raise ValueError('SSID phải dài 1–32 byte UTF-8, không có dấu nháy kép, dấu gạch chéo ngược hoặc ký tự điều khiển (giới hạn DietPi).')
    return ssid


def psk(ssid, password):
    if isinstance(password, str) and re.fullmatch(r'[0-9a-fA-F]{64}', password):
        return password.lower()
    if not isinstance(password, str) or not re.fullmatch(r'[\x20-\x7e]{8,63}', password):
        raise ValueError('Mật khẩu WPA phải có 8–63 ký tự ASCII in được, hoặc khóa PSK gồm 64 ký tự hex.')
    return hashlib.pbkdf2_hmac('sha1', password.encode(), ssid.encode(), 4096, 32).hex()


def parse_db(raw):
    slots = [empty_slot() for _ in range(SLOTS)]
    seen = set()
    for line in raw.decode('utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = re.fullmatch(r'aWIFI_([A-Z0-9_]+)\[([0-4])\]=(.*)', line)
        if not match or match[1] not in FIELDS:
            raise ValueError('WiFi DB có định dạng khác DietPi chuẩn; chưa sửa cấu hình.')
        key, index = match[1], int(match[2])
        if (key, index) in seen:
            raise ValueError('WiFi DB có mục trùng lặp; cần kiểm tra bằng dietpi-config.')
        seen.add((key, index))
        try:
            parts = shlex.split(match[3], comments=True)
        except ValueError:
            raise ValueError('Không đọc được định dạng WiFi DB; chưa sửa cấu hình.') from None
        if len(parts) > 1:
            raise ValueError('WiFi DB không phải các giá trị đơn; chưa sửa cấu hình.')
        slots[index][key] = parts[0] if parts else ''
    names = []
    for item in slots:
        if not item['SSID']:
            continue
        validate_ssid(item['SSID'])
        names.append(item['SSID'])
        if item['KEYMGR'] not in ('WPA-PSK', 'NONE') or any(item[k] for k in FIELDS[3:]):
            raise ValueError('Bản này chỉ hỗ trợ WiFi cá nhân WPA/WPA2-PSK hoặc mạng mở. Cấu hình WEP/EAP/tùy chỉnh cần dùng dietpi-config.')
    if len(set(names)) != len(names):
        raise ValueError('SSID trùng nhau trong DietPi DB; cần kiểm tra bằng dietpi-config.')
    return slots


def serialize(slots):
    # Quote every value, never source or eval incoming data.
    return ''.join(f'aWIFI_{key}[{i}]={shlex.quote(item[key])}\n'
                   for i, item in enumerate(slots) for key in FIELDS).encode()


def expected_networks(slots):
    result = []
    for item in slots:
        if item['SSID']:
            network = {'ssid': '"' + item['SSID'] + '"', 'scan_ssid': '1', 'key_mgmt': item['KEYMGR']}
            if item['KEYMGR'] == 'WPA-PSK':
                network['psk'] = item['KEY'] if re.fullmatch(r'[0-9a-fA-F]{64}', item['KEY']) else psk(item['SSID'], item['KEY'])
            result.append(network)
    return result


def check_wpa(raw, slots, country):
    globals_, networks, block = {}, [], None
    for line in raw.decode('utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line == 'network={' and block is None:
            block = {}
        elif line == '}' and block is not None:
            networks.append(block)
            block = None
        elif '=' in line:
            key, value = line.split('=', 1)
            target = globals_ if block is None else block
            if key in target:
                raise ValueError('Cấu hình WiFi trùng khóa; chưa sửa cấu hình.')
            target[key] = value
        else:
            raise ValueError('Cấu hình WiFi tùy chỉnh; chưa sửa cấu hình.')
    expected_globals = {'country': country, 'ctrl_interface': 'DIR=/run/wpa_supplicant GROUP=netdev', 'update_config': '1'}
    if block is not None or globals_ != expected_globals or networks != expected_networks(slots):
        raise ValueError('wpa_supplicant.conf và DietPi DB không khớp định dạng chuẩn. Chưa thay đổi; kiểm tra WiFi trong dietpi-config trước.')


def read_file(path):
    if path.is_symlink():
        raise ValueError('File cấu hình WiFi là symlink; chưa thay đổi.')
    with path.open('rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError('Cấu hình WiFi không phải file thông thường.')
        raw = stream.read(128 * 1024 + 1)
    if len(raw) > 128 * 1024:
        raise ValueError('File cấu hình WiFi vượt giới hạn hỗ trợ.')
    return raw


def write_private(path, raw):
    fd, name = tempfile.mkstemp(prefix='.pi-control-wifi-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class DietPiWiFi:
    def __init__(self, root=Path('/')):
        self.root = Path(root)
        self.db = self.root / 'var/lib/dietpi/dietpi-wifi.db'
        self.wpa = self.root / 'etc/wpa_supplicant/wpa_supplicant.conf'
        self.helper = self.root / 'boot/dietpi/func/dietpi-wifidb'
        self.settings = self.root / 'boot/dietpi.txt'

    def load(self):
        if not all(p.is_file() for p in (self.db, self.wpa, self.helper, self.settings)):
            raise ValueError('Chưa tìm thấy đầy đủ cấu hình DietPi WiFi. Hãy thiết lập wlan0 một lần bằng dietpi-config trước.')
        if (self.root / 'boot/dietpi-wifi.txt').exists():
            raise ValueError('DietPi còn file WiFi khởi tạo; hoàn tất dietpi-config trước khi thêm mạng.')
        helper = read_file(self.helper).decode()
        if not re.search(r'readonly MAX_SSID_SLOTS=5\b', helper) or 'Wifi_Db_Apply()' not in helper:
            raise ValueError('Phiên bản dietpi-wifidb chưa được hỗ trợ; chưa thay đổi.')
        settings = read_file(self.settings)
        matches = re.findall(rb'^\s*AUTO_SETUP_NET_WIFI_COUNTRY_CODE=([A-Z]{2})\s*$', settings, re.M)
        if len(matches) != 1:
            raise ValueError('Cần đặt mã quốc gia WiFi trong dietpi-config trước.')
        country = matches[0].decode()
        db, wpa = read_file(self.db), read_file(self.wpa)
        slots = parse_db(db)
        check_wpa(wpa, slots, country)
        revision = hashlib.sha256(db + b'\0' + wpa + b'\0' + settings).hexdigest()
        return slots, db, wpa, country, revision

    def status(self):
        slots, _, _, country, revision = self.load()
        return {'networks': [{'slot': i + 1, 'ssid': v['SSID'], 'security': v['KEYMGR']}
                             for i, v in enumerate(slots) if v['SSID']],
                'capacity': SLOTS, 'country': country, 'revision': revision}

    def generate(self):
        proc = subprocess.Popen(['bash', str(self.helper), '1'], stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                start_new_session=True)
        try:
            if proc.wait(timeout=25) != 0:
                raise ValueError('DietPi không tạo được cấu hình WiFi.')
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise ValueError('DietPi tạo cấu hình quá thời gian cho phép.') from None

    def save(self, data):
        ssid = validate_ssid(data.get('ssid'))
        security = data.get('security', 'WPA-PSK')
        if security not in ('WPA-PSK', 'NONE'):
            raise ValueError('Kiểu bảo mật WiFi không hỗ trợ.')
        key = psk(ssid, data.get('password')) if security == 'WPA-PSK' else ''
        slots, db, wpa, country, revision = self.load()
        if data.get('revision') != revision:
            raise ValueError('Cấu hình WiFi đã đổi. Bấm Đọc mạng đã lưu rồi thử lại.')
        index = next((i for i, item in enumerate(slots) if item['SSID'] == ssid), None)
        updating = index is not None
        if updating and data.get('replace') is not True:
            raise ValueError('SSID đã lưu. Chọn cập nhật mạng trùng tên để đổi mật khẩu.')
        if index is None:
            index = next((i for i, item in enumerate(slots) if not item['SSID']), None)
        if index is None:
            raise ValueError('Đã đầy 5 mạng WiFi. Không xóa mạng cũ; quản lý vị trí bằng dietpi-config.')
        slots[index] = {**empty_slot(), 'SSID': ssid, 'KEYMGR': security, 'KEY': key}
        # Normalize pre-existing PSKs too, so native wpa_passphrase never receives
        # plaintext credentials in process arguments.
        for item in slots:
            if item['SSID'] and item['KEYMGR'] == 'WPA-PSK':
                item['KEY'] = psk(item['SSID'], item['KEY'])
        backup = Path(tempfile.mkdtemp(prefix='pi-control-wifi-backup-', dir=self.db.parent))
        write_private(backup / 'dietpi-wifi.db', db)
        write_private(backup / 'wpa_supplicant.conf', wpa)
        if self.load()[4] != revision:
            raise ValueError('Cấu hình WiFi vừa đổi; chưa ghi đè.')
        try:
            write_private(self.db, serialize(slots))
            self.generate()
            result_slots, _, _, _, _ = self.load()
            if result_slots != slots:
                raise ValueError('DietPi trả về cấu hình khác dữ liệu cần lưu.')
        except Exception:
            write_private(self.db, db)
            write_private(self.wpa, wpa)
            raise ValueError('Không lưu được WiFi; đã khôi phục hai file cấu hình cũ. Chưa nạp lại mạng.') from None
        return {**self.status(), 'message': 'Đã cập nhật WiFi' if updating else 'Đã thêm WiFi',
                'backup': str(backup), 'saved_ssid': ssid,
                'note': 'Đã lưu trên Pi. Chưa nạp lại kết nối; mật khẩu chưa được kiểm chứng bằng kết nối thực tế.'}

    def reload(self, data):
        if data.get('confirm') is not True:
            raise ValueError('Cần xác nhận việc nạp lại mạng có thể làm mất SSH tạm thời.')
        if data.get('revision') != self.load()[4]:
            raise ValueError('Cấu hình đã đổi; đọc lại danh sách trước khi áp dụng.')
        cli = shutil.which('wpa_cli')
        if not cli or not (self.root / 'sys/class/net/wlan0/wireless').is_dir():
            raise ValueError('Không tìm thấy wpa_cli hoặc WiFi wlan0 đang được hỗ trợ.')
        result = subprocess.run([cli, '-i', 'wlan0', 'ping'], capture_output=True, timeout=5)
        if result.returncode or b'PONG' not in result.stdout:
            raise ValueError('wpa_supplicant trên wlan0 chưa phản hồi. Kiểm tra dietpi-config.')
        # Separate process survives the SSH session if WiFi changes. No passwords.
        code = 'import subprocess,time; time.sleep(3); subprocess.run([' + repr(cli) + ", '-i', 'wlan0', 'reconfigure'], timeout=15)"
        subprocess.Popen([sys.executable, '-c', code], stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True, close_fds=True)
        return {'message': 'Đã hẹn nạp danh sách WiFi sau 3 giây. SSH/Tailscale có thể ngắt tạm thời; đây chưa phải xác nhận kết nối thành công.'}


def operate(data):
    if os.geteuid() != 0:
        raise ValueError('Chức năng WiFi DietPi cần đăng nhập SSH bằng root.')
    adapter = DietPiWiFi()
    # Serializes this tool across clients; dietpi-config does not use this lock.
    fd = os.open('/run/lock/pi-control-wifi.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Đang có thao tác WiFi khác; thử lại sau.') from None
        if data.get('action') == 'status':
            return adapter.status()
        if data.get('action') == 'save':
            return adapter.save(data)
        if data.get('action') == 'reload':
            return adapter.reload(data)
        raise ValueError('Thao tác WiFi không hợp lệ.')


if __name__ == '__main__':
    try:
        print(json.dumps(operate(json.load(sys.stdin)), ensure_ascii=False))
    except ValueError as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
    except Exception:
        # OS/subprocess exceptions must not echo WiFi secrets or raw file data.
        print(json.dumps({'error': 'Không đọc/ghi được cấu hình DietPi WiFi. Kiểm tra quyền root, dung lượng và trạng thái DietPi.'}, ensure_ascii=False))
