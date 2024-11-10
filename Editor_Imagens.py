import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imagens")
        self.root.geometry("650x900")
        self.root.configure(bg="#2A2F38")

        # Variáveis de imagem e filtros
        self.original_image = None
        self.filtered_image = None
        self.brightness_value = 1.0
        self.contrast_value = 1.0
        
        # Header estilo Telegram
        self.header_frame = tk.Frame(root, bg="#2A2F38")
        self.header_frame.pack(fill=tk.X, pady=10)

        self.title_label = tk.Label(
            self.header_frame, text="Editor de Imagens", font=("Arial", 16, "bold"), 
            bg="#2A2F38", fg="#FFFFFF"
        )
        self.title_label.pack(pady=5)

        # Botão de abrir imagem
        self.open_button = tk.Button(
            root, text="📂 Abrir Imagem", command=self.open_image, 
            bg="#4A90E2", fg="#FFFFFF", font=("Arial", 12), relief=tk.FLAT
        )
        self.open_button.pack(pady=10)

        # Frame de filtros
        self.filters_frame = tk.Frame(root, bg="#2A2F38")
        self.filters_frame.pack(pady=10)

        # Botões de filtros
        self.gray_button = self.create_filter_button("Escala de Cinza", self.apply_gray_filter)
        self.negative_button = self.create_filter_button("Negativo", self.apply_negative_filter)
        self.blur_button = self.create_filter_button("Desfoque", self.apply_blur_filter)
        self.vintage_button = self.create_filter_button("Vintage", self.apply_vintage_filter)
        self.retro_button = self.create_filter_button("Retro", self.apply_retro_filter)
        self.drama_button = self.create_filter_button("Drama", self.apply_drama_filter)
        self.soft_focus_button = self.create_filter_button("Soft Focus", self.apply_soft_focus_filter)

        # Brilho
        self.brightness_frame = self.create_adjustment_frame("Brilho", self.decrease_brightness, self.increase_brightness)
        # Contraste
        self.contrast_frame = self.create_adjustment_frame("Contraste", self.decrease_contrast, self.increase_contrast)

        # Botão de salvar
        self.save_button = tk.Button(
            root, text="💾 Salvar Imagem", command=self.save_image, 
            bg="#27AE60", fg="#FFFFFF", font=("Arial", 12), relief=tk.FLAT, state=tk.DISABLED
        )
        self.save_button.pack(pady=20)

        # Label para exibir a imagem
        self.image_label = tk.Label(root, bg="#2A2F38")
        self.image_label.pack(pady=10)

    def create_filter_button(self, text, command):
        button = tk.Button(
            self.filters_frame, text=text, command=command, 
            bg="#4A4F5A", fg="#FFFFFF", font=("Arial", 10), width=12, relief=tk.FLAT, state=tk.DISABLED
        )
        button.grid(padx=5, pady=5)
        return button

    def create_adjustment_frame(self, text, minus_command, plus_command):
        frame = tk.Frame(self.root, bg="#2A2F38")
        frame.pack(pady=5)

        label = tk.Label(frame, text=text + ":", font=("Arial", 10), bg="#2A2F38", fg="#FFFFFF")
        label.pack(side=tk.LEFT, padx=5)

        minus_button = tk.Button(frame, text="-", command=minus_command, 
                                 bg="#4A4F5A", fg="#FFFFFF", relief=tk.FLAT, width=3, state=tk.DISABLED)
        minus_button.pack(side=tk.LEFT, padx=5)

        plus_button = tk.Button(frame, text="+", command=plus_command, 
                                bg="#4A4F5A", fg="#FFFFFF", relief=tk.FLAT, width=3, state=tk.DISABLED)
        plus_button.pack(side=tk.LEFT, padx=5)
        
        # Atribui botões para ativação posterior
        if text == "Brilho":
            self.brightness_minus_button = minus_button
            self.brightness_plus_button = plus_button
        elif text == "Contraste":
            self.contrast_minus_button = minus_button
            self.contrast_plus_button = plus_button

        return frame

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.filtered_image = self.original_image.copy()
            self.display_image(self.filtered_image)
            self.enable_buttons()

    def display_image(self, img):
        img = img.copy()
        img.thumbnail((800, 800))  # Define o tamanho padrão para 800x800
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def enable_buttons(self):
        # Habilita todos os botões de filtros e ajustes
        buttons = [
            self.gray_button, self.negative_button, self.blur_button, 
            self.vintage_button, self.retro_button, self.drama_button, 
            self.soft_focus_button, self.save_button,
            self.brightness_minus_button, self.brightness_plus_button,
            self.contrast_minus_button, self.contrast_plus_button
        ]
        for button in buttons:
            button.config(state=tk.NORMAL)

    def apply_filter(self, filter_function):
        if self.filtered_image:
            self.filtered_image = filter_function(self.original_image)
            self.display_image(self.filtered_image)

    def apply_gray_filter(self):
        self.apply_filter(ImageOps.grayscale)

    def apply_negative_filter(self):
        self.apply_filter(lambda img: ImageOps.invert(img.convert("RGB")))

    def apply_blur_filter(self):
        self.apply_filter(lambda img: img.filter(ImageFilter.BLUR))

    def apply_vintage_filter(self):
        self.apply_filter(lambda img: img.convert("L").point(lambda x: x * 0.9).convert("RGB"))

    def apply_retro_filter(self):
        def retro_effect(img):
            img = img.convert("RGB")
            img = ImageEnhance.Color(img).enhance(0.5)
            img = ImageEnhance.Contrast(img).enhance(0.8)
            r, g, b = img.split()
            r = r.point(lambda i: i * 1.2)
            g = g.point(lambda i: i * 1.1)
            img = Image.merge("RGB", (r, g, b))
            return img
        self.apply_filter(retro_effect)

    def apply_drama_filter(self):
        def drama_effect(img):
            enhancer_contrast = ImageEnhance.Contrast(img)
            img = enhancer_contrast.enhance(1.8)
            enhancer_sharpness = ImageEnhance.Sharpness(img)
            return enhancer_sharpness.enhance(2.0)
        self.apply_filter(drama_effect)

    def apply_soft_focus_filter(self):
        self.apply_filter(lambda img: img.filter(ImageFilter.SMOOTH_MORE))

    def adjust_brightness(self):
        enhancer = ImageEnhance.Brightness(self.original_image)
        self.filtered_image = enhancer.enhance(self.brightness_value)
        self.display_image(self.filtered_image)

    def adjust_contrast(self):
        enhancer = ImageEnhance.Contrast(self.original_image)
        self.filtered_image = enhancer.enhance(self.contrast_value)
        self.display_image(self.filtered_image)

    def increase_brightness(self):
        if self.brightness_value < 2.0:
            self.brightness_value += 0.1
            self.adjust_brightness()

    def decrease_brightness(self):
        if self.brightness_value > 0.0:
            self.brightness_value -= 0.1
            self.adjust_brightness()

    def increase_contrast(self):
        if self.contrast_value < 2.0:
            self.contrast_value += 0.1
            self.adjust_contrast()

    def decrease_contrast(self):
        if self.contrast_value > 0.5:
            self.contrast_value -= 0.1
            self.adjust_contrast()

    def save_image(self):
        if self.filtered_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                self.filtered_image.save(file_path)
                messagebox.showinfo("Imagem Salva", "A imagem foi salva com sucesso!")

root = tk.Tk()
app = ImageEditorApp(root)
root.mainloop()
