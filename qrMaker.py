import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image

def generate_qr_with_logo(url, logo_path, qr_output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    logo = Image.open(logo_path)
    logo = logo.convert("RGBA")

    qr_size = img.size[0]
    logo_size = int(qr_size * 0.3)
    logo = logo.resize((logo_size, logo_size))

    logo_position = (qr_size // 2 - logo_size // 2, qr_size // 2 - logo_size // 2)
    img.paste(logo, logo_position, mask=logo)

    img.save(qr_output_path)

def gui():
    root = tk.Tk()
    root.title("QR Code Generator")

    def browse_logo():
        file_path = filedialog.askopenfilename()
        logo_path_var.set(file_path)

    def browse_output():
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        output_path_var.set(file_path)

    def generate_qr():
        url = url_var.get()
        logo_path = logo_path_var.get()
        output_path = output_path_var.get()

        if url and logo_path and output_path:
            generate_qr_with_logo(url, logo_path, output_path)
            status_var.set("QR code generated successfully!")
        else:
            status_var.set("Please fill in all fields and try again.")

    # Create input fields and buttons
    url_var = tk.StringVar()
    logo_path_var = tk.StringVar()
    output_path_var = tk.StringVar()
    status_var = tk.StringVar()

    tk.Label(root, text="URL:").grid(row=0, column=0, sticky="e")
    tk.Entry(root, textvariable=url_var, width=40).grid(row=0, column=1)
    tk.Label(root, text="Logo Path:").grid(row=1, column=0, sticky="e")
    tk.Entry(root, textvariable=logo_path_var, width=40).grid(row=1, column=1)
    tk.Button(root, text="Browse", command=browse_logo).grid(row=1, column=2)
    tk.Label(root, text="Output Path:").grid(row=2, column=0, sticky="e")
    tk.Entry(root, textvariable=output_path_var, width=40).grid(row=2, column=1)
    tk.Button(root, text="Browse", command=browse_output).grid(row=2, column=2)
    tk.Button(root, text="Generate QR Code", command=generate_qr).grid(row=3, column=1)
    tk.Label(root, textvariable=status_var).grid(row=4, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    gui()
