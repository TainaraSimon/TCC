import qrcode

LINK = "https://introspect-fiyw.onrender.com"  

qr = qrcode.QRCode(box_size=12, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(LINK)
qr.make(fit=True)

imagem = qr.make_image(fill_color="#030303ff", back_color="white")
imagem.save("qrcode_introspect.png")
print("QR code salvo em qrcode_introspect.png")