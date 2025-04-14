import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import Qt
from scanner import get_ip_range, is_host_alive, scan_ports, detect_os, port_to_service


class NmapScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI 类Nmap扫描器")
        self.setGeometry(800, 200, 1000, 1000)  # 设置窗口大小和位置:
        self.setWindowIcon(QIcon("resources/logo.ico"))  # 可选
        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f5;
                font-family: "Segoe UI";
            }
            QLineEdit, QTextEdit {
                background: white;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 8px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # IP 段输入
        ip_layout = QHBoxLayout()
        self.start_ip = QLineEdit()
        self.start_ip.setPlaceholderText("起始 IP (如 192.168.1.1)")
        self.end_ip = QLineEdit()
        self.end_ip.setPlaceholderText("结束 IP (如 192.168.1.10)")
        ip_layout.addWidget(self.start_ip)
        ip_layout.addWidget(self.end_ip)

        # 端口输入
        port_layout = QHBoxLayout()
        self.port_start = QLineEdit("1")
        self.port_end = QLineEdit("1024")
        port_layout.addWidget(QLabel("端口范围："))
        port_layout.addWidget(self.port_start)
        port_layout.addWidget(QLabel("到"))
        port_layout.addWidget(self.port_end)

        # 线程滑块
        thread_layout = QHBoxLayout()
        self.thread_slider = QSlider(Qt.Horizontal)
        self.thread_slider.setMinimum(10)
        self.thread_slider.setMaximum(300)
        self.thread_slider.setValue(100)
        self.thread_label = QLabel("线程数：100")
        self.thread_slider.valueChanged.connect(
            lambda val: self.thread_label.setText(f"线程数：{val}")
        )
        thread_layout.addWidget(self.thread_label)
        thread_layout.addWidget(self.thread_slider)

        # 扫描按钮、导出按钮
        button_layout = QHBoxLayout()
        self.scan_button = QPushButton("开始扫描")
        self.scan_button.clicked.connect(self.start_scan)
        self.export_button = QPushButton("导出结果")
        self.export_button.clicked.connect(self.export_result)
        button_layout.addWidget(self.scan_button)
        button_layout.addWidget(self.export_button)

        # 动态 loading 动画
        self.loading = QLabel()
        self.loading.setAlignment(Qt.AlignCenter)
        self.loading_movie = QMovie("resources/loading3.gif")
        self.loading.setMovie(self.loading_movie)
        self.loading.setFixedSize(60, 60)  # 设置GIF动画的尺寸为60x60像素
        self.loading_movie.setCacheMode(QMovie.CacheAll)  # 缓存所有帧
        self.loading.hide()  # 默认不显示

        # 输出框
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        # 进度条
        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addLayout(ip_layout)
        layout.addLayout(port_layout)
        layout.addLayout(thread_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress)
        layout.addWidget(self.loading)
        layout.addWidget(self.result_box)
        self.setLayout(layout)

    def log(self, text):
        self.result_box.append(text)
        QApplication.processEvents()

    def start_scan(self):
        self.scan_button.setEnabled(False)
        self.scan_button.setText("正在扫描...")
        self.loading.show()
        self.loading_movie.start()
        self.result_box.clear()
        self.progress.setValue(0)

        start = self.start_ip.text()
        end = self.end_ip.text()

        try:
            port_range = range(int(self.port_start.text()), int(self.port_end.text()) + 1)
            thread_count = self.thread_slider.value()
        except:
            self.log("❌ 输入错误！")
            self.scan_button.setEnabled(True)
            self.loading_movie.stop()
            self.loading.hide()
            return

        ip_list = get_ip_range(start, end)
        if not ip_list:
            self.log("❌ IP 范围错误！")
            self.scan_button.setEnabled(True)
            self.loading_movie.stop()
            self.loading.hide()
            return

        total_hosts = len(ip_list)
        self.log(f"🌐 扫描范围：{start} 到 {end}，端口 {port_range.start}-{port_range.stop - 1}，线程数：{thread_count}\n")

        self.scan_results = ""

        for idx, ip in enumerate(ip_list, 1):
            self.log("-".center(100, "-"))
            self.log(f"🔎 正在扫描主机 {ip} ...")
            self.scan_results += f"主机 {ip}：\n"

            if not is_host_alive(ip):
                self.log(f"❌ 主机 {ip} 不在线\n")
                self.scan_results += f"状态：离线\n\n"
            else:
                self.log(f"✅ 主机 {ip} 在线")
                os_info = detect_os(ip)
                self.log(f"🖥️ 操作系统识别：{os_info}")
                self.log(f"⚡ 正在扫描端口，请稍候...")
                open_ports = scan_ports(ip, port_range, thread_count)
                if open_ports:
                    ports_str = ", ".join([f"{p} ({port_to_service(p)})" for p in open_ports])
                else:
                    ports_str = "无开放端口"
                self.log(f"📍 开放端口：{ports_str}\n")
                self.scan_results += f"状态：在线\n操作系统：{os_info}\n开放端口：{ports_str}\n\n"

            self.progress.setValue(int((idx / total_hosts) * 100))

        self.scan_button.setEnabled(True)
        self.scan_button.setText("重新扫描")
        self.loading_movie.stop()
        self.loading.hide()
        self.log("✅ 所有主机扫描完成！")

    def export_result(self):
        if not hasattr(self, 'scan_results') or not self.scan_results.strip():
            QMessageBox.warning(self, "导出失败", "没有可导出的扫描结果。")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "保存扫描结果", "scan_result.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.scan_results)
            QMessageBox.information(self, "导出成功", f"扫描结果已保存到：\n{filename}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NmapScanner()
    window.show()
    sys.exit(app.exec_())
