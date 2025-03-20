import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import time

class PhotoBooth:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Photo Booth")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Inisialisasi kamera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Tidak dapat mengakses kamera!")
            exit()
        
        # Ambil resolusi kamera
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Direktori untuk menyimpan foto
        self.save_dir = "photo_booth_images"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # Status dan variabel program
        self.current_frame = None
        self.last_photo = None
        self.countdown_active = False
        self.countdown_value = 3
        self.current_filter = "normal"
        self.available_filters = {
            "normal": "Normal",
            "grayscale": "Hitam Putih",
            "sepia": "Sepia",
            "cartoon": "Kartun",
            "negative": "Negatif",
            "blur": "Blur",
            "edge": "Deteksi Tepi"
        }
        
        # Frame untuk menampilkan tampilan kamera
        self.camera_frame = ttk.Frame(self.root)
        self.camera_frame.pack(pady=10)
        
        # Canvas untuk menampilkan gambar dari kamera
        self.canvas = tk.Canvas(self.camera_frame, width=self.width, height=self.height)
        self.canvas.pack()
        
        # Frame untuk tombol-tombol
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        # Tombol ambil foto
        self.capture_btn = ttk.Button(self.button_frame, text="Ambil Foto (Space)", command=self.start_countdown)
        self.capture_btn.grid(row=0, column=0, padx=5)
        
        # Dropdown untuk filter
        self.filter_label = ttk.Label(self.button_frame, text="Filter:")
        self.filter_label.grid(row=0, column=1, padx=5)
        
        self.filter_var = tk.StringVar()
        self.filter_var.set("normal")
        
        self.filter_menu = ttk.Combobox(self.button_frame, textvariable=self.filter_var, 
                                       values=list(self.available_filters.values()),
                                       state="readonly", width=15)
        self.filter_menu.current(0)
        self.filter_menu.grid(row=0, column=2, padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.change_filter)
        
        # Tombol save foto terakhir
        self.save_btn = ttk.Button(self.button_frame, text="Simpan Foto (S)", command=self.save_photo)
        self.save_btn.grid(row=0, column=3, padx=5)
        self.save_btn.config(state="disabled")  # Disable sampai foto diambil
        
        # Bind keyboard shortcuts
        self.root.bind("<space>", lambda e: self.start_countdown())
        self.root.bind("s", lambda e: self.save_photo())
        
        # Status bar untuk informasi
        self.status_var = tk.StringVar()
        self.status_var.set("Siap untuk mengambil foto")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Memulai update frame kamera
        self.update_frame()
        
        # Pastikan kamera ditutup saat program ditutup
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def update_frame(self):
        """Update frame dari kamera dan tampilkan di canvas"""
        ret, frame = self.cap.read()
        
        if ret:
            # Flip horizontal agar seperti cermin
            frame = cv2.flip(frame, 1)
            
            # Simpan frame saat ini
            self.current_frame = frame.copy()
            
            # Terapkan filter
            processed_frame = self.apply_filter(frame)
            
            # Jika countdown aktif, tampilkan angka countdown
            if self.countdown_active:
                cv2.putText(processed_frame, str(self.countdown_value), 
                           (int(self.width/2) - 50, int(self.height/2) + 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 8)
            
            # Konversi frame dari BGR ke RGB
            rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            # Konversi ke format yang bisa ditampilkan di Tkinter
            img = Image.fromarray(rgb_frame)
            img_tk = ImageTk.PhotoImage(image=img)
            
            # Update canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk  # Keep a reference
        
        # Schedule the next update
        self.root.after(10, self.update_frame)
    
    def apply_filter(self, frame):
        """Terapkan filter ke frame"""
        filter_name = self.get_filter_key_from_value(self.filter_var.get())
        
        if filter_name == "grayscale":
            return cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        
        elif filter_name == "sepia":
            sepia_kernel = np.array([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])
            sepia_image = cv2.transform(frame, sepia_kernel)
            sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
            return sepia_image
        
        elif filter_name == "cartoon":
            # Buat efek kartun
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                         cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(frame, 9, 300, 300)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            return cartoon
        
        elif filter_name == "negative":
            return 255 - frame
        
        elif filter_name == "blur":
            return cv2.GaussianBlur(frame, (15, 15), 0)
        
        elif filter_name == "edge":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        else:  # Normal
            return frame
    
    def get_filter_key_from_value(self, filter_value):
        """Mendapatkan kunci filter dari nilainya"""
        for key, value in self.available_filters.items():
            if value == filter_value:
                return key                
        return "normal"  # Default
    
    def start_countdown(self):
        """Mulai countdown untuk mengambil foto"""
        if not self.countdown_active:
            self.countdown_active = True
            self.countdown_value = 3
            self.status_var.set(f"Siap-siap! Countdown: {self.countdown_value}")
            self.root.after(1000, self.update_countdown)
    
    def update_countdown(self):
        """Update nilai countdown dan ambil foto ketika mencapai 0"""
        self.countdown_value -= 1
        
        if self.countdown_value > 0:
            self.status_var.set(f"Siap-siap! Countdown: {self.countdown_value}")
            self.root.after(1000, self.update_countdown)
        else:
            self.capture_photo()
    
    def capture_photo(self):
        """Ambil foto dan tampilkan"""
        # Ambil frame saat ini dan terapkan filter
        if self.current_frame is not None:
            self.last_photo = self.apply_filter(self.current_frame.copy())
            
            # Buat suara jepretan kamera
            print("\a")  # Beep sistem
            
            # Update status
            self.status_var.set("Foto berhasil diambil! Tekan 'Simpan Foto' untuk menyimpan.")
            
            # Aktifkan tombol simpan
            self.save_btn.config(state="normal")
        
        self.countdown_active = False
    
    def save_photo(self):
        """Simpan foto terakhir yang diambil"""
        if self.last_photo is not None:
            # Buat nama file unik dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filter_name = self.get_filter_key_from_value(self.filter_var.get())
            filename = f"{self.save_dir}/photo_booth_{filter_name}_{timestamp}.jpg"
            
            # Simpan gambar
            cv2.imwrite(filename, self.last_photo)
            
            # Update status
            self.status_var.set(f"Foto disimpan sebagai {filename}")
    
    def change_filter(self, event=None):
        """Callback ketika filter berubah"""
        self.status_var.set(f"Filter berubah ke: {self.filter_var.get()}")
    
    def on_close(self):
        """Tutup kamera dan jendela saat program ditutup"""
        self.cap.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = PhotoBooth(root)
    root.mainloop()

if __name__ == "__main__":
    main()