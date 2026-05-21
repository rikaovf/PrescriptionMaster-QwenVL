import os
import torch

from PIL import Image

from config import HF_MODELS_DIR

# =========================================================
# HUGGINGFACE CACHE
# =========================================================

os.environ["HF_HOME"] = HF_MODELS_DIR
os.environ["TRANSFORMERS_CACHE"] = HF_MODELS_DIR
os.environ["HUGGINGFACE_HUB_CACHE"] = HF_MODELS_DIR

# =========================================================
# TRANSFORMERS
# =========================================================

from transformers import (
    AutoProcessor,
    Qwen2VLForConditionalGeneration
)

# =========================================================
# CONFIG
# =========================================================

MODEL_ID = "Qwen/Qwen2-VL-2B-Instruct"

# =========================================================
# DEVICE AUTO
# =========================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[INFO] Device selecionado: {device}")

# =========================================================
# LOAD PROCESSOR
# =========================================================

print("[INFO] Carregando processor...")

processor = AutoProcessor.from_pretrained(
    MODEL_ID
)

# =========================================================
# LOAD MODEL
# =========================================================

print("[INFO] Carregando Qwen2-VL 2B...")

# =========================================================
# CONFIG GPU
# =========================================================

if device == "cuda":

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,

        torch_dtype=torch.float16,

        device_map="cuda",

        low_cpu_mem_usage=True,

        attn_implementation="sdpa"
    )

# =========================================================
# CONFIG CPU
# =========================================================

else:

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,

        torch_dtype=torch.float32,

        device_map="cpu",

        low_cpu_mem_usage=True
    )

# =========================================================
# EVAL MODE
# =========================================================

model.eval()

print("[INFO] Modelo carregado com sucesso")

# =========================================================
# PROMPT OCR
# =========================================================

SYSTEM_PROMPT = """
Você é um OCR especializado em receitas médicas.

Sua função é extrair TODO o texto da imagem.

REGRAS:
- NÃO interpretar
- NÃO resumir
- NÃO reorganizar
- NÃO corrigir
- NÃO explicar

Preserve:
- linhas
- espaçamentos
- enumeração
- dosagens
- observações
- separação entre fórmulas
- manuscritos mesmo com baixa confiança

Retorne SOMENTE o texto bruto extraído.
"""

# =========================================================
# EXTRAÇÃO MULTIMODAL
# =========================================================

def extrair_texto_qwen(image_path: str):

    # =====================================================
    # LOAD IMAGE
    # =====================================================

    image = Image.open(image_path).convert("RGB")

    # =====================================================
    # OTIMIZAÇÃO
    # =====================================================

    # reduz explosão de patches visuais
    image.thumbnail((1400, 1400))

    # =====================================================
    # CHAT TEMPLATE
    # =====================================================

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image"
                },
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT
                }
            ]
        }
    ]

    text_prompt = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # =====================================================
    # PROCESSAMENTO MULTIMODAL
    # =====================================================

    inputs = processor(
        text=[text_prompt],
        images=[image],
        padding=True,
        return_tensors="pt"
    )

    # =====================================================
    # DEVICE
    # =====================================================

    inputs = {
        k: v.to(device)
        if hasattr(v, "to")
        else v
        for k, v in inputs.items()
    }

    # =====================================================
    # INFERÊNCIA
    # =====================================================

    with torch.inference_mode():

        generated_ids = model.generate(
            **inputs,

            # OCR não precisa exagero
            max_new_tokens=256,

            # inferência estável
            do_sample=False,

            # reduz consumo VRAM/RAM
            use_cache=False
        )

    # =====================================================
    # REMOVE PROMPT TOKENS
    # =====================================================

    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(
            inputs["input_ids"],
            generated_ids
        )
    ]

    # =====================================================
    # DECODE
    # =====================================================

    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )[0]

    # =====================================================
    # LIMPEZA
    # =====================================================

    output_text = output_text.strip()

    # =====================================================
    # LIMPA VRAM
    # =====================================================

    if device == "cuda":
        torch.cuda.empty_cache()

    return output_text