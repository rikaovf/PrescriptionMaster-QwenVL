import torch
import os

os.environ["HF_HOME"] = HF_MODELS_DIR

from PIL import Image
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

MODEL_ID = "Qwen/Qwen2-VL-7B-Instruct"

# =========================r
# 1. DEVICE INTELIGENTE
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# 2. CARREGAMENTO SINGLETON
# =========================0659232
print("[INFO] Carregando Qwen-VL (uma vez só)...")

processor = AutoProcessor.from_pretrained(MODEL_ID)

model = Qwen2VLForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    device_map="auto",
    low_cpu_mem_usage=True
)

model.eval()  # 🔥 importante: modo inferência


SYSTEM_PROMPT = """
Você é um OCR especializado em receitas médicas.

Extraia o texto exatamente como aparece na imagem.
- não interprete
- não explique
- não resuma
- preserve linhas e enumeração
"""


def extrair_texto_qwen(image_path: str):

    image = Image.open(image_path).convert("RGB")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": SYSTEM_PROMPT}
            ]
        }
    ]

    # =========================
    # 3. PREPROCESSAMENTO
    # =========================
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    )

    #inputs = inputs.to(device)
    inputs = processor(
    text=SYSTEM_PROMPT,
    images=image,
    return_tensors="pt"
    )

    inputs = {
        k: v.to(device)
        if hasattr(v, "to")
        else v
        for k, v in inputs.items()
    }

    # =========================
    # 4. INFERÊNCIA OTIMIZADA
    # =========================
    with torch.no_grad():  # 🔥 evita uso de memória desnecessária

        output = model.generate(
            **inputs,
            max_new_tokens=512,   # 🔥 reduz RAM e tempo
            temperature=0.1,
            do_sample=False       # 🔥 mais estável e leve
        )

    # =========================
    # 5. DECODIFICAÇÃO
    # =========================
    result = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    # limpeza leve
    return result.strip()