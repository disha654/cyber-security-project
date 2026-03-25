import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import stego_engine

# Theme Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SteganoApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Steganography Tool")
        self.geometry("900x700")

        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. HEADER SECTION
        self.header_frame = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="🔒 LSB STEGANOGRAPHY", 
                                        font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(side="top", pady=(0, 5))
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Hide secret data inside images securely.", 
                                           font=ctk.CTkFont(size=14), text_color="gray")
        self.subtitle_label.pack(side="top")

        # 2. MAIN CONTENT (Tabs)
        self.tabview = ctk.CTkTabview(self, width=850, height=550, 
                                     segmented_button_fg_color="gray20",
                                     segmented_button_selected_color="#1f538d",
                                     segmented_button_unselected_hover_color="gray30")
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.tab_encode = self.tabview.add("ENCODE DATA")
        self.tab_decode = self.tabview.add("DECODE DATA")

        self.setup_encode_tab()
        self.setup_decode_tab()

    def setup_encode_tab(self):
        tab = self.tab_encode
        tab.grid_columnconfigure(0, weight=1)

        # Card 1: Image Selection
        self.img_card_encode = ctk.CTkFrame(tab, fg_color="gray15", corner_radius=15)
        self.img_card_encode.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.img_card_encode.grid_columnconfigure(0, weight=1)

        self.drop_label_encode = ctk.CTkLabel(self.img_card_encode, 
                                             text="📂 Drop Image Here or Click to Browse", 
                                             height=120, corner_radius=10, fg_color="gray25",
                                             font=ctk.CTkFont(size=16, weight="bold"),
                                             cursor="hand2")
        self.drop_label_encode.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.drop_label_encode.drop_target_register(DND_FILES)
        self.drop_label_encode.dnd_bind('<<Drop>>', self.handle_drop_encode)
        self.drop_label_encode.bind("<Button-1>", lambda e: self.browse_image_encode())

        self.encode_image_path = ctk.StringVar()
        self.status_encode = ctk.CTkLabel(self.img_card_encode, text="No image selected", 
                                         text_color="gray70", font=ctk.CTkFont(size=12))
        self.status_encode.grid(row=1, column=0, pady=(0, 15))

        # Card 2: Message Input
        self.msg_card = ctk.CTkFrame(tab, fg_color="gray15", corner_radius=15)
        self.msg_card.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.msg_card.grid_columnconfigure(0, weight=1)

        self.msg_title = ctk.CTkLabel(self.msg_card, text="Secret Message", 
                                     font=ctk.CTkFont(size=14, weight="bold"))
        self.msg_title.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.message_input = ctk.CTkTextbox(self.msg_card, height=180, corner_radius=10, 
                                           border_width=2, border_color="gray30")
        self.message_input.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Action Button
        self.encode_btn = ctk.CTkButton(tab, text="🚀 HIDE DATA & SAVE IMAGE", 
                                       height=50, corner_radius=10, 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       command=self.process_encode)
        self.encode_btn.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

    def setup_decode_tab(self):
        tab = self.tab_decode
        tab.grid_columnconfigure(0, weight=1)

        # Card 1: Image Selection
        self.img_card_decode = ctk.CTkFrame(tab, fg_color="gray15", corner_radius=15)
        self.img_card_decode.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.img_card_decode.grid_columnconfigure(0, weight=1)

        self.drop_label_decode = ctk.CTkLabel(self.img_card_decode, 
                                             text="🔍 Drop Modified Image Here", 
                                             height=120, corner_radius=10, fg_color="gray25",
                                             font=ctk.CTkFont(size=16, weight="bold"),
                                             cursor="hand2")
        self.drop_label_decode.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.drop_label_decode.drop_target_register(DND_FILES)
        self.drop_label_decode.dnd_bind('<<Drop>>', self.handle_drop_decode)
        self.drop_label_decode.bind("<Button-1>", lambda e: self.browse_image_decode())

        self.decode_image_path = ctk.StringVar()
        self.status_decode = ctk.CTkLabel(self.img_card_decode, text="No image selected", 
                                         text_color="gray70", font=ctk.CTkFont(size=12))
        self.status_decode.grid(row=1, column=0, pady=(0, 15))

        # Card 2: Output Display
        self.output_card = ctk.CTkFrame(tab, fg_color="gray15", corner_radius=15)
        self.output_card.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.output_card.grid_columnconfigure(0, weight=1)

        self.output_title = ctk.CTkLabel(self.output_card, text="Extracted Message", 
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.output_title.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.output_display = ctk.CTkTextbox(self.output_card, height=180, corner_radius=10, 
                                            border_width=2, border_color="gray30")
        self.output_display.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Action Button
        self.decode_btn = ctk.CTkButton(tab, text="🔓 EXTRACT HIDDEN DATA", 
                                       height=50, corner_radius=10, 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       command=self.process_decode)
        self.decode_btn.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

    # Handlers (Same logic, better UI updates)
    def handle_drop_encode(self, event):
        path = event.data.strip('{}')
        if self.is_image(path):
            self.encode_image_path.set(path)
            self.status_encode.configure(text=f"✅ Selected: {os.path.basename(path)}", text_color="#2ecc71")
        else:
            messagebox.showerror("Error", "Invalid file format. Use PNG, BMP, or JPG.")

    def handle_drop_decode(self, event):
        path = event.data.strip('{}')
        if self.is_image(path):
            self.decode_image_path.set(path)
            self.status_decode.configure(text=f"✅ Selected: {os.path.basename(path)}", text_color="#2ecc71")
        else:
            messagebox.showerror("Error", "Invalid file format. Use PNG, BMP, or JPG.")

    def browse_image_encode(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.bmp *.jpg *.jpeg")])
        if path:
            self.encode_image_path.set(path)
            self.status_encode.configure(text=f"✅ Selected: {os.path.basename(path)}", text_color="#2ecc71")

    def browse_image_decode(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.bmp *.jpg *.jpeg")])
        if path:
            self.decode_image_path.set(path)
            self.status_decode.configure(text=f"✅ Selected: {os.path.basename(path)}", text_color="#2ecc71")

    def is_image(self, path):
        return path.lower().endswith(('.png', '.bmp', '.jpg', '.jpeg'))

    def process_encode(self):
        if not self.encode_image_path.get():
            messagebox.showwarning("Warning", "Please select an image first.")
            return
        
        msg = self.message_input.get("1.0", "end-1c")
        if not msg:
            messagebox.showwarning("Warning", "Please enter a secret message.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                filetypes=[("PNG Image (Lossless)", "*.png")])
        if save_path:
            success, result = stego_engine.encode_data(self.encode_image_path.get(), msg, save_path)
            if success:
                messagebox.showinfo("Success", "Data hidden successfully!\nFile saved as: " + os.path.basename(save_path))
            else:
                messagebox.showerror("Error", result)

    def process_decode(self):
        if not self.decode_image_path.get():
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        success, data, data_type = stego_engine.decode_data(self.decode_image_path.get())
        if success:
            if data_type == "text":
                self.output_display.delete("1.0", "end")
                self.output_display.insert("1.0", data)
                messagebox.showinfo("Success", "Hidden message extracted!")
            else:
                # Fallback for binary data
                save_file = filedialog.asksaveasfilename(title="Save extracted data")
                if save_file:
                    with open(save_file, "wb") as f:
                        f.write(data)
                    messagebox.showinfo("Success", "File extracted successfully!")
        else:
            messagebox.showerror("Error", "No hidden data found or invalid format.")

if __name__ == "__main__":
    app = SteganoApp()
    app.mainloop()
