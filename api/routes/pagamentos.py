from fastapi import APIRouter
import qrcode
import io
import base64

router = APIRouter()

@router.get("/pagamento/qrcode/{pedido_id}")
def gerar_qrcode(pedido_id: int):
    # Simulação de um payload Pix ou URL de pagamento
    payload = f"pix://chave-pix?pedido_id={pedido_id}"

    # Geração do QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Converter para base64
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {"status": "sucesso", "qrcode_base64": img_str}