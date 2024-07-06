import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

def generate_qr(data, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4, fill_color="black", back_color="white", style="default"):
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)

    if style == "rounded":
        img = qr.make_image(fill_color=fill_color, back_color=back_color, image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    else:
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

    return img
