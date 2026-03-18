import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np


# -----------------------------
# Conversii cerute în laborator
# -----------------------------

def rgb_to_gray1(img):
    # Gray(1) = (R+G+B)/3
    return np.uint8(np.mean(img, axis=2))


def rgb_to_gray2(img):
    # Gray(2) = 0.299*R + 0.587*G + 0.114*B
    return np.uint8(0.299 * img[:, :, 2] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 0])


def rgb_to_gray3(img):
    # Gray(3) = (min(R,G,B) + max(R,G,B)) / 2
    min_val = np.min(img, axis=2)
    max_val = np.max(img, axis=2)
    return np.uint8((min_val + max_val) / 2)


def rgb_to_cmy(img):
    # Convertim BGR -> RGB
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # C = 1 - R/255, etc.
    cmy = 1 - (rgb / 255.0)

    # Convertim înapoi la 0–255 pentru afișare
    cmy_255 = np.uint8(cmy * 255)

    return cmy_255


# -----------------------------
# Funcția de încărcare imagine
# -----------------------------

def open_image():
    file_path = filedialog.askopenfilename(
        title="Alege o imagine",
        filetypes=[("Image files", "*.bmp;*.png;*.jpg;*.jpeg"), ("All files", "*.*")]
    )

    if not file_path:
        print("Nu ai selectat nicio imagine.")
        return

    img = cv2.imread(file_path)
    if img is None:
        print("Eroare la citirea imaginii.")
        return

    print("Imagine încărcată:", file_path)
    cv2.imshow("Original", img)

    # -----------------------------
    # Generăm imaginile grayscale
    # -----------------------------
    gray1 = rgb_to_gray1(img)
    gray2 = rgb_to_gray2(img)
    gray3 = rgb_to_gray3(img)

    cv2.imshow("Gray 1 - (R+G+B)/3", gray1)
    cv2.imshow("Gray 2 - formula ponderată", gray2)
    cv2.imshow("Gray 3 - (min+max)/2", gray3)

    # -----------------------------
    # Conversie RGB -> CMY
    # -----------------------------
    cmy = rgb_to_cmy(img)
    cv2.imshow("CMY", cmy)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# -----------------------------
# Interfața grafică Tkinter
# -----------------------------

root = tk.Tk()
root.title("Procesare Imagini - Laborator")

btn = tk.Button(root, text="Încarcă imagine", command=open_image, width=30, height=2)
btn.pack(pady=20)

root.mainloop()
