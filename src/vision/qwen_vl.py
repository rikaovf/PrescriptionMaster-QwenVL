import os
import gc
import time
import torch

from PIL import Image

from config import HF_MODELS_DIR
from prompts.visionocr_prompt import PROMPT
from vision.image_enhancer import melhorar_imagem

# =========================================================
# CACHE HUGGINGFACE
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
# DEVICE
# =========================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[INFO] Device: {device}")

if device == "cuda":

    print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")

    # evita consumir 100% da VRAM
    torch.cuda.set_per_process_memory_fraction(0.90)

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

print("[INFO] Carregando modelo Qwen2-VL...")

if device == "cuda":

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        attn_implementation="sdpa"
    ).to(device)

else:

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    ).to(device)

# =========================================================
# EVAL MODE
# =========================================================

model.eval()

print("[INFO] Modelo carregado")


# =========================================================
# DEBUG MEMÓRIA
# =========================================================

def mostrar_memoria():

    if device == "cuda":

        memoria_alocada = (
            torch.cuda.memory_allocated() / 1024**3
        )

        memoria_reservada = (
            torch.cuda.memory_reserved() / 1024**3
        )

        print(
            f"[GPU] VRAM Alocada: "
            f"{memoria_alocada:.2f} GB"
        )

        print(
            f"[GPU] VRAM Reservada: "
            f"{memoria_reservada:.2f} GB"
        )

# =========================================================
# OCR MULTIMODAL
# =========================================================

def extrair_texto_qwen(image_path: str):

    print("\n[ETAPA 1] Qwen-VL extraindo texto...")

    inicio = time.time()

    image = Image.open(image_path).convert("RGB")
    image = melhorar_imagem(image)
    image.thumbnail((1600, 1600))

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {
                    "type": "text",
                    "text": PROMPT
                }
            ]
        }
    ]

    text_prompt = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text_prompt],
        images=[image],
        padding=True,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(device)
        if hasattr(v, "to")
        else v
        for k, v in inputs.items()
    }

    mostrar_memoria()

    with torch.inference_mode():

        generated_ids = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            use_cache=True
        )

    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(
            inputs["input_ids"],
            generated_ids
        )
    ]

    output_text = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )[0]

    output_text = output_text.strip()

    del inputs
    del generated_ids
    del generated_ids_trimmed

    gc.collect()

    if device == "cuda":
        torch.cuda.empty_cache()

    fim = time.time()

    print(
        f"\n[INFO] Tempo OCR Total: "
        f"{(fim - inicio):.2f}s"
    )

    return output_text