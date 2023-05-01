import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, EpsImagePlugin
import os

def generate_qr_with_logo(url, logo_path, qr_output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=1,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    logo = Image.open(logo_path)
    logo = logo.convert("RGBA")

    qr_size = img.size[0]
    logo_size = int(qr_size * 0.3)
    logo = logo.resize((logo_size, logo_size))

    logo_position = (qr_size // 2 - logo_size // 2, qr_size // 2 - logo_size // 2)
    img.paste(logo, logo_position, mask=logo)

    # Save QR code as an EPS file
    eps_output_path = os.path.splitext(qr_output_path)[0] + '.eps'
    img.save(eps_output_path, 'EPS', compression='none', fill_rule='evenodd')

def gui():
    root = tk.Tk()
    root.title("QR Code Generator")
    root.configure(bg="white")
    root.geometry("+30+30")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)

    def browse_output():
        file_path = filedialog.asksaveasfilename(defaultextension=".eps")
        output_path_var.set(file_path)

    def generate_qr():
        url = url_var.get()
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        output_path = output_path_var.get()

        if url and logo_path and output_path:
            generate_qr_with_logo(url, logo_path, output_path)
            status_var.set("QR code generated successfully!")
        else:
            status_var.set("Please fill in all fields and try again.")

    # Create input fields and buttons
    url_var = tk.StringVar()
    output_path_var = tk.StringVar()
    status_var = tk.StringVar()

    font_label = ("Verdana", 12)
    font_entry = ("Verdana", 10)
    font_button = ("Verdana", 10)

    tk.Label(root, text="URL:", font=font_label, bg="white").grid(row=0, column=0, sticky="e", pady=10)
    tk.Entry(root, textvariable=url_var, width=40, font=font_entry).grid(row=0, column=1, pady=10)
    tk.Label(root, text="Output Path:", font=font_label, bg="white").grid(row=1, column=0, sticky="e", pady=10)
    tk.Entry(root, textvariable=output_path_var, width=40, font=font_entry).grid(row=1, column=1, pady=10)
    
    browse_button = tk.Button(root, text="Browse", command=browse_output, bg="#43B02A", fg="#fff", font=font_button, relief="flat", padx=12, pady=6)
    browse_button.grid(row=1, column=2, padx=5, pady=10)

    generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr, bg="#43B02A", fg="#fff", font=font_button, relief="flat", padx=12, pady=6)
    generate_button.grid(row=2, column=1, pady=20)

    tk.Label(root, textvariable=status_var, bg="white", font=font_label).grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == '__main__':
    gui()