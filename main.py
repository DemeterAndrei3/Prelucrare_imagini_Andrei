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
#--------------------------------
#Lab_3
#----------------------------------

# ---------------------------------------------------------
# 1. Conversie RGB → YUV și YCbCr
# ---------------------------------------------------------

def convert_to_YUV(image):
    # OpenCV folosește BGR, deci convertim întâi în RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    yuv = cv2.cvtColor(rgb, cv2.COLOR_RGB2YUV)
    return yuv

def convert_to_YCbCr(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ycbcr = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)  # OpenCV folosește YCrCb
    return ycbcr

# ---------------------------------------------------------
# 2. Imagine inversă + afișarea canalelor
# ---------------------------------------------------------

def inverse_image(image):
    inverted = 255 - image
    return inverted

def show_channels(image, title_prefix="Channel"):
    b, g, r = cv2.split(image)
    plt.figure(figsize=(12,4))
    plt.subplot(1,3,1); plt.imshow(b, cmap='gray'); plt.title(f"{title_prefix} - B")
    plt.subplot(1,3,2); plt.imshow(g, cmap='gray'); plt.title(f"{title_prefix} - G")
    plt.subplot(1,3,3); plt.imshow(r, cmap='gray'); plt.title(f"{title_prefix} - R")
    plt.show()

# ---------------------------------------------------------
# 3. Binarizare imagine
# ---------------------------------------------------------

def binarize(image, threshold=128):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary

# ---------------------------------------------------------
# 4. Calcul centru de masă
# ---------------------------------------------------------

def center_of_mass(binary_image):
    # Convertim în imagine binară 0/1
    img = binary_image // 255

    # Coordonate
    h, w = img.shape
    y_indices, x_indices = np.indices((h, w))

    # Formula centrului de masă
    total = img.sum()
    if total == 0:
        return None

    x_center = (x_indices * img).sum() / total
    y_center = (y_indices * img).sum() / total

    return (x_center, y_center)

# ---------------------------------------------------------
# Program principal
# ---------------------------------------------------------

image = cv2.imread("imagine.jpg")  # pune numele imaginii tale

# 1. Conversii
yuv = convert_to_YUV(image)
ycbcr = convert_to_YCbCr(image)

plt.figure(figsize=(10,4))
plt.subplot(1,2,1); plt.imshow(yuv); plt.title("YUV")
plt.subplot(1,2,2); plt.imshow(ycbcr); plt.title("YCbCr")
plt.show()

# 2. Imagine inversă + canale
inv = inverse_image(image)
show_channels(inv, "Inverted")

# 3. Binarizare
binary = binarize(image, threshold=120)
plt.imshow(binary, cmap='gray'); plt.title("Imagine binarizată"); plt.show()

# 4. Centru de masă
center = center_of_mass(binary)
print("Centrul de masă:", center)

# Afișare centru pe imagine
if center:
    img_copy = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_copy, (int(center[0]), int(center[1])), 5, (0,0,255), -1)
    plt.imshow(img_copy); plt.title("Centru de masă"); plt.show(
root.mainloop()
