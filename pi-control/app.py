"""Pi Control — launch with python3 app.py (or --demo)."""
import json
from pathlib import Path
import queue
import shlex
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from core import SSH, service_command

CONFIG = Path.home() / '.pi-control.json'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('AI Green · Pi Control')
        self.geometry('1180x780')
        self.minsize(900, 620)
        self.client = None
        self.busy = False
        self.events = queue.Queue()
        self.service_rows = []
        self.demo = '--demo' in sys.argv
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', font=('Arial', 11))
        style.configure('TButton', padding=(10, 7))
        style.configure('Card.TLabel', font=('Arial', 18, 'bold'), padding=15, background='#e5f2ec')
        style.configure('Treeview', rowheight=29)
        style.configure('Title.TLabel', font=('Arial', 23, 'bold'), foreground='#126b50')
        top = ttk.Frame(self, padding=16)
        top.pack(fill='x')
        ttk.Label(top, text='AI Green / Pi Control', style='Title.TLabel').pack(side='left')
        self.status = tk.StringVar(value='Chưa kết nối · Nhập Tailscale khi sẵn sàng')
        ttk.Label(top, textvariable=self.status).pack(side='right')
        conn = ttk.LabelFrame(self, text='Kết nối SSH qua Tailscale', padding=10)
        conn.pack(fill='x', padx=16)
        defaults = {'host': '', 'user': 'dietpi', 'port': '22', 'key': '', 'telemetry': '/opt/thiennhan/history/telemetry.json'}
        try:
            saved = json.loads(CONFIG.read_text())
            defaults.update({k: str(saved[k]) for k in defaults if k in saved})
        except (OSError, ValueError, TypeError):
            pass
        self.fields = {}
        for i, (key, label, width) in enumerate([('host', 'IP / hostname', 25), ('user', 'User', 12),
                                                ('port', 'Port', 6), ('key', 'SSH key (tùy chọn)', 28)]):
            f = ttk.Frame(conn)
            f.pack(side='left', padx=5)
            ttk.Label(f, text=label).pack(anchor='w')
            self.fields[key] = tk.StringVar(value=defaults[key])
            ttk.Entry(f, textvariable=self.fields[key], width=width).pack()
        ttk.Button(conn, text='Kết nối', command=self.connect).pack(side='left', padx=6, pady=12)
        ttk.Button(conn, text='Ngắt', command=self.disconnect).pack(side='left')
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill='both', expand=True, padx=16, pady=12)
        self.pages = {}
        for name in ['Tổng quan', 'Services', 'Thiết bị', 'Cảm biến', 'Thu âm', 'Lệnh & log']:
            page = ttk.Frame(self.tabs, padding=12)
            self.tabs.add(page, text=name)
            self.pages[name] = page
        overview = self.pages['Tổng quan']
        self.cards = {}
        for i, name in enumerate(['CPU', 'RAM', 'Ổ đĩa', 'Nhiệt độ']):
            value = tk.StringVar(value=f'{name}\n—')
            self.cards[name] = value
            ttk.Label(overview, textvariable=value, style='Card.TLabel').grid(row=0, column=i, padx=5, sticky='ew')
            overview.columnconfigure(i, weight=1)
        self.summary = tk.StringVar(value='Dữ liệu cập nhật mỗi 5 giây. Chưa có dữ liệu thực từ Pi.')
        ttk.Label(overview, textvariable=self.summary, wraplength=950, justify='left').grid(row=1, column=0, columnspan=4, sticky='w', pady=25)
        ttk.Button(overview, text='Làm mới', command=self.refresh).grid(row=2, column=0, sticky='w')
        ttk.Label(overview, text='Bật/tắt hiện tại và tự chạy khi khởi động là hai trạng thái riêng.\nThiết bị I²C/GPIO cần telemetry từ driver để xác nhận dữ liệu; có bus không đồng nghĩa có cảm biến.\nỨng dụng không lấy hình ảnh camera.', wraplength=940, justify='left').grid(row=3, column=0, columnspan=4, sticky='w', pady=25)
        page = self.pages['Services']
        toolbar = ttk.Frame(page)
        toolbar.pack(fill='x')
        self.search = tk.StringVar()
        ttk.Entry(toolbar, textvariable=self.search, width=25).pack(side='left')
        self.search.trace_add('write', lambda *_: self.render_services())
        for label, action in [('Chạy', 'start'), ('Dừng', 'stop'), ('Khởi động lại', 'restart'),
                              ('Tự chạy', 'enable'), ('Bỏ tự chạy', 'disable'), ('Xem log', 'logs')]:
            ttk.Button(toolbar, text=label, command=lambda a=action: self.service_action(a)).pack(side='left', padx=2)
        self.services = self.tree(page, ('Service', 'Trạng thái', 'Chi tiết', 'Khởi động', 'Mô tả'), (280, 100, 100, 110, 340))
        self.device_text = self.textbox(self.pages['Thiết bị'], 'Quét lại thiết bị', self.scan_devices)
        page = self.pages['Cảm biến']
        row = ttk.Frame(page)
        row.pack(fill='x')
        ttk.Label(row, text='Telemetry JSON trên Pi:').pack(side='left')
        self.telemetry_path = tk.StringVar(value=defaults['telemetry'])
        ttk.Entry(row, textvariable=self.telemetry_path, width=55).pack(side='left', padx=8)
        ttk.Button(row, text='Đọc lại', command=self.refresh).pack(side='left')
        self.sensor_status = tk.StringVar(value='Chưa có dữ liệu')
        ttk.Label(page, textvariable=self.sensor_status).pack(anchor='w', pady=10)
        self.sensor_tree = self.tree(page, ('Thiết bị / trường', 'Giá trị'), (400, 580))
        page = self.pages['Thu âm']
        ttk.Label(page, text='Thu trên Pi → lưu WAV trên máy tính. Mono 16-bit.\nNếu service đang dùng mic, dừng service đó trước khi thu thử. Không tự dừng service.', justify='left').pack(anchor='w', pady=10)
        self.audio = {}
        for name, label, default in [('device', 'Thiết bị ALSA (xem tab Thiết bị)', 'default'), ('seconds', 'Thời lượng (1–120 giây)', '5'), ('rate', 'Tần số (16000 / 44100 / 48000 Hz)', '16000')]:
            ttk.Label(page, text=label).pack(anchor='w', pady=(10, 2))
            self.audio[name] = tk.StringVar(value=default)
            ttk.Entry(page, textvariable=self.audio[name], width=45).pack(anchor='w')
        ttk.Button(page, text='Thu âm và lưu WAV…', command=self.record).pack(anchor='w', pady=20)
        self.record_status = tk.StringVar(value='Chưa thu âm')
        ttk.Label(page, textvariable=self.record_status).pack(anchor='w')
        page = self.pages['Lệnh & log']
        ttk.Label(page, text='Lệnh chạy trên Pi bằng user SSH; tối đa 30 giây. Không hỗ trợ lệnh tương tác / nhập mật khẩu.').pack(anchor='w')
        self.command = tk.StringVar(value='uptime')
        ttk.Entry(page, textvariable=self.command).pack(fill='x', pady=10)
        self.logs = self.textbox(page, 'Chạy lệnh…', self.run_command)
        self.after(100, self.drain)
        self.after(5000, self.tick)
        if self.demo:
            self.after(100, self.show_demo)

    def tree(self, parent, columns, widths):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, pady=10)
        tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
        for column, width in zip(columns, widths):
            tree.heading(column, text=column)
            tree.column(column, width=width, minwidth=60)
        scroll = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        return tree

    def textbox(self, parent, label, command):
        ttk.Button(parent, text=label, command=command).pack(anchor='w', pady=5)
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        text = tk.Text(frame, wrap='word', font=('Courier', 11), bg='#102b29', fg='#d8f0e6', state='disabled')
        bar = ttk.Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=bar.set)
        bar.pack(side='right', fill='y')
        text.pack(fill='both', expand=True)
        return text

    def write(self, widget, content):
        widget.configure(state='normal')
        widget.delete('1.0', 'end')
        widget.insert('end', content)
        widget.configure(state='disabled')

    def submit(self, label, operation, callback):
        if self.busy:
            return False
        if not self.client:
            messagebox.showinfo('Chưa kết nối', 'Nhập địa chỉ Pi và bấm Kết nối.')
            return False
        self.busy = True
        self.status.set(label + '…')
        def worker():
            try:
                self.events.put((callback, operation(), None))
            except Exception as exc:
                self.events.put((callback, None, str(exc)))
        threading.Thread(target=worker, daemon=True).start()
        return True

    def drain(self):
        try:
            callback, value, error = self.events.get_nowait()
            self.busy = False
            if error:
                self.status.set('Thao tác lỗi · xem Lệnh & log')
                self.write(self.logs, error)
                self.summary.set('Lần cập nhật/thao tác thất bại. Số liệu đang hiển thị là lần đọc trước, không phải dữ liệu trực tiếp.')
                self.sensor_status.set('Chưa xác nhận dữ liệu mới — xem lỗi tại Lệnh & log')
                self.record_status.set('Thao tác kết thúc với lỗi — xem Lệnh & log')
            else:
                self.status.set('SSH phản hồi · ' + time.strftime('%H:%M:%S'))
                callback(value)
        except queue.Empty:
            pass
        self.after(100, self.drain)

    def connect(self):
        if self.busy:
            return
        try:
            values = {key: value.get().strip() for key, value in self.fields.items()}
            client = SSH(values['host'], values['user'], int(values['port']), values['key'])
            client.argv()
            self.client = client
            self.demo = False
            CONFIG.write_text(json.dumps({**values, 'telemetry': self.telemetry_path.get()}, indent=2))
            self.refresh()
        except (OSError, ValueError) as exc:
            messagebox.showerror('Cấu hình', str(exc))

    def disconnect(self):
        if self.busy:
            messagebox.showinfo('Đang thao tác', 'Đợi thao tác hiện tại kết thúc rồi ngắt kết nối.')
            return
        self.client = None
        self.status.set('Đã ngắt · dữ liệu hiển thị là lần đọc cuối')
        self.sensor_status.set('Đã ngắt — dữ liệu lưu từ lần đọc trước')

    def refresh(self):
        if self.demo:
            self.show_demo()
        elif self.client and not self.busy:
            client, path = self.client, self.telemetry_path.get()
            self.submit('Đang đọc Pi', lambda: client.probe('snapshot', path), self.render)

    def tick(self):
        self.refresh()
        self.after(5000, self.tick)

    def render(self, data):
        for name, key in [('CPU', 'cpu_percent'), ('RAM', 'ram_percent'), ('Ổ đĩa', 'disk_percent'), ('Nhiệt độ', 'temperature_c')]:
            value = data.get(key)
            self.cards[name].set(name + '\n' + ('—' if value is None else f'{value}{" °C" if name == "Nhiệt độ" else "%"}'))
        self.summary.set(f"{data['hostname']} · Uptime {data['uptime_seconds']/3600:.1f} giờ · Load {data['load']}\n"
                         f"Lần đọc: {time.strftime('%H:%M:%S')} · {len(data['services']['rows'])} service\n" + '\n'.join(data['services']['errors']))
        selection = self.services.item(self.services.selection()[0], 'values')[0] if self.services.selection() else None
        self.service_rows = data['services']['rows']
        self.render_services(selection)
        telemetry = data['telemetry']
        self.sensor_status.set({'fresh': 'Dữ liệu mới', 'stale': 'DỮ LIỆU CŨ — không dùng như giá trị hiện tại', 'unavailable': 'Chưa có telemetry'}[telemetry['state']] + f" · Tuổi mẫu: {telemetry.get('age_seconds', '—')} giây · {telemetry.get('error', '')}")
        self.sensor_tree.delete(*self.sensor_tree.get_children())
        def flatten(value, prefix=''):
            if isinstance(value, dict):
                for key, item in value.items():
                    flatten(item, f'{prefix}.{key}' if prefix else key)
            else:
                self.sensor_tree.insert('', 'end', values=(prefix, 'Không có mẫu / lỗi đọc' if value is None else str(value)))
        flatten(telemetry.get('data', {}).get('devices', {}))

    def render_services(self, selected=None):
        if selected is None and self.services.selection():
            selected = self.services.item(self.services.selection()[0], 'values')[0]
        self.services.delete(*self.services.get_children())
        for row in self.service_rows:
            if self.search.get().lower() in ' '.join(row).lower():
                item = self.services.insert('', 'end', values=row)
                if row[0] == selected:
                    self.services.selection_set(item)

    def service_action(self, action):
        if not self.services.selection() or self.busy:
            return
        unit = self.services.item(self.services.selection()[0], 'values')[0]
        try:
            command = service_command(action, unit)
        except ValueError as exc:
            messagebox.showerror('Service', str(exc))
            return
        if action != 'logs' and not messagebox.askyesno('Điều khiển service', f'{action}: {unit}?'):
            return
        client = self.client
        def done(raw):
            self.write(self.logs, raw.decode(errors='replace') or f'{action} {unit}: thành công')
            if action == 'logs':
                self.tabs.select(self.pages['Lệnh & log'])
            else:
                self.refresh()
        self.submit(f'{action} {unit}', lambda: client.execute(command), done)

    def scan_devices(self):
        client, path = self.client, self.telemetry_path.get()
        self.submit('Đọc danh sách thiết bị', lambda: client.probe('devices', path), lambda data:
                    self.write(self.device_text, '\n\n'.join(f'[{name}] {"" if value["ok"] else "KHÔNG ĐỌC ĐƯỢC"}\n{value["text"]}' for name, value in data.items())))

    def run_command(self):
        if self.busy:
            return
        command = self.command.get().strip()
        if not command or not messagebox.askyesno('Chạy lệnh trên Pi', command):
            return
        client = self.client
        wrapped = shlex.join(['timeout', '--signal=TERM', '--kill-after=2', '30', 'sh', '-lc', command])
        self.submit('Chạy lệnh', lambda: client.execute(wrapped), lambda raw: self.write(self.logs, raw.decode(errors='replace') or '(không có output)'))

    def record(self):
        if self.busy or not self.client:
            return
        try:
            seconds, rate = int(self.audio['seconds'].get()), int(self.audio['rate'].get())
            if not 1 <= seconds <= 120 or rate not in {16000, 44100, 48000}:
                raise ValueError('Thu 1–120 giây; tần số 16000 / 44100 / 48000 Hz')
        except ValueError as exc:
            messagebox.showerror('Thu âm', str(exc))
            return
        path = filedialog.asksaveasfilename(defaultextension='.wav', filetypes=[('WAV', '*.wav')], initialfile='pi-recording.wav')
        if not path:
            return
        client, device = self.client, self.audio['device'].get()
        self.record_status.set(f'Đang thu {seconds} giây…')
        def done(raw):
            if not (raw[:4] == b'RIFF' and raw[8:12] == b'WAVE'):
                self.record_status.set('Pi trả dữ liệu không phải WAV; chưa lưu')
                return
            try:
                Path(path).write_bytes(raw)
                self.record_status.set(f'Đã lưu: {path}')
            except OSError as exc:
                self.record_status.set(f'Không lưu được: {exc}')
        self.submit('Thu âm', lambda: client.record(device, seconds, rate), done)

    def show_demo(self):
        self.status.set('DEMO · dữ liệu minh họa, không kết nối Pi')
        self.render({'hostname': 'pi-demo (DỮ LIỆU GIẢ LẬP)', 'cpu_percent': 18.4, 'ram_percent': 42.1,
                     'disk_percent': 28.6, 'temperature_c': 46.2, 'uptime_seconds': 7200, 'load': [0.2, 0.3, 0.2],
                     'services': {'rows': [['thiennhan.service', 'active', 'running', 'enabled', 'Thiên Nhãn'],
                     ['tailscaled.service', 'active', 'running', 'enabled', 'Tailscale'],
                     ['example.service', 'inactive', 'dead', 'disabled', 'Ví dụ']], 'errors': []},
                     'telemetry': {'state': 'fresh', 'age_seconds': 0, 'data': {'devices': {'imu': {'roll_deg': 1.2, 'pitch_deg': -2.4}, 'distance': {'distance_mm': 530}}}}})
        self.sensor_status.set('DEMO — mẫu minh họa, không phải cảm biến thật')


if __name__ == '__main__':
    App().mainloop()
