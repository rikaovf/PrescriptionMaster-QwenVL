import os
import gc
import time
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

if device == "cuda":

    print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")

    # evita explosão total da VRAM
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

print("[INFO] Carregando Qwen2-VL 2B...")

# =========================================================
# GPU
# =========================================================

if device == "cuda":

    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_ID,

        torch_dtype=torch.float16,

        low_cpu_mem_usage=True,

        attn_implementation="sdpa"
    ).to(device)

# =========================================================
# CPU
# =========================================================

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

print("[INFO] Modelo carregado com sucesso")

# =========================================================
# PROMPT OCR
# =========================================================

SYSTEM_PROMPT = """
Você é um OCR especializado em receitas médicas brasileiras.

Sua função é extrair TODO o texto presente na imagem.

IMPORTANTE:
Dê atenção especial para:

- nome do paciente
- nome do médico
- CRM
- telefone
- cabeçalhos
- rodapés
- carimbos
- observações
- posologia
- fórmulas manipuladas

REGRAS:
- NÃO resumir
- NÃO explicar
- NÃO reorganizar
- NÃO inventar
- NÃO interpretar

Extraia exatamente como estiver escrito.

Preserve:
- linhas
- enumerações
- dosagens
- símbolos
- observações
- separação entre fórmulas

Retorne SOMENTE o texto extraído.
"""

# =========================================================
# DEBUG MEMÓRIA
# =========================================================

def mostrar_memoria():

    if device == "cuda":

        alocada = torch.cuda.memory_allocated() / (1024 ** 3)

        reservada = torch.cuda.memory_reserved() / (1024 ** 3)

        print(f"[GPU] VRAM Alocada: {alocada:.2f} GB")

        print(f"[GPU] VRAM Reservada: {reservada:.2f} GB")

# =========================================================
# EXTRAÇÃO MULTIMODAL
# =========================================================

def extrair_texto_qwen(image_path: str):

    print("\n[ETAPA 1] Qwen-VL extraindo texto...")

    tempo_inicio = time.time()

    # =====================================================
    # LOAD IMAGE
    # =====================================================

    image = Image.open(image_path).convert("RGB")

    # =====================================================
    # OTIMIZAÇÃO
    # =====================================================

    # MUITO IMPORTANTE:
    # reduz drasticamente patches visuais
    image.thumbnail((1024, 1024))

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
    # PROCESSAMENTO
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

    mostrar_memoria()

    # =====================================================
    # INFERÊNCIA
    # =====================================================

    with torch.inference_mode():

        generated_ids = model.generate(
            **inputs,

            # importante para velocidade
            max_new_tokens=128,

            # OCR precisa estabilidade
            do_sample=False,

            # MUITO MAIS RÁPIDO
            use_cache=True
        )

    # =====================================================
    # REMOVE TOKENS DO PROMPT
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

    output_text = output_text.strip()

    # =====================================================
    # LIMPEZA MEMÓRIA
    # =====================================================

    del inputs
    del generated_ids
    del generated_ids_trimmed

    gc.collect()

    if device == "cuda":
        torch.cuda.empty_cache()

    # =====================================================
    # TEMPO TOTAL
    # =====================================================

    tempo_total = time.time() - tempo_inicio

    print(f"[INFO] Tempo OCR: {tempo_total:.2f}s")

    mostrar_memoria()

    return output_text