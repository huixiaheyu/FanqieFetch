"""手动确认字库识别的 GUI 界面。

当自动 OCR 识别不准确时，弹窗展示图片与识别结果，
支持按键快速确认或手动修改。
"""

import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


class UI:
    def __init__(self, image, file_name, ocr_result, stop_loop):
        """辅助识别图片中的文字，识别错误时手动更改。

        Args:
            image: PIL Image 对象。
            file_name: 图片名。
            ocr_result: OCR 识别结果。
            stop_loop: 是否停止循环识别（传引用，按 ESC 后置 True）。
        """
        self.file_name = file_name
        self.image = image
        self.ocr_result = ocr_result
        self.final_result = None
        self.stop_loop = stop_loop

        self.root = tk.Tk()
        self.root.title("(快捷键)确认: Enter；修改: Space；退出: Esc")
        self.root.attributes("-topmost", True)
        self.root.focus_force()

        # 窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width, window_height = 370, 300
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 3
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.image_resized = ImageTk.PhotoImage(self.image.resize((170, 170)))

        label1 = tk.Label(self.root, text="真实图片", font=("Arial", 10, "bold"))
        label1.grid(row=0, column=0, padx=10, pady=2, sticky="ew")
        label2 = tk.Label(self.root, text="识别结果", font=("Arial", 10, "bold"))
        label2.grid(row=0, column=1, padx=10, pady=2, sticky="ew")

        img_label = tk.Label(self.root, image=self.image_resized)
        img_label.grid(row=1, column=0, padx=10, pady=10)

        text_label = tk.Label(self.root, text=self.ocr_result, font=("Arial", 80, "bold"))
        text_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.input_entry = ttk.Entry(self.root, width=45)
        self.input_entry.grid(row=2, columnspan=2, padx=10, pady=5, sticky="ew")

        self.confirm_button = ttk.Button(self.root, text="确认", command=self.confirm)
        self.confirm_button.grid(row=3, column=0, padx=10, pady=10)
        modify_button = ttk.Button(self.root, text="更改", command=self.modify)
        modify_button.grid(row=3, column=1, padx=10, pady=10)

        self.root.bind("<KeyPress>", self.on_keypress)
        self.root.mainloop()

    def on_keypress(self, event):
        if event.keysym == "Return":
            self.confirm()
        elif event.keysym == "space":
            self.modify()
        elif event.keysym == "Escape":
            self.cancel()

    def confirm(self):
        self.final_result = self.input_entry.get() or self.ocr_result
        self.root.destroy()

    def modify(self):
        self.input_entry.focus_set()

    def cancel(self):
        self.stop_loop = True
        self.root.destroy()
