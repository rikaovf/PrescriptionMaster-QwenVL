#from transformers import Qwen2VLForConditionalGeneration
import torch

print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())

if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))

#print("Carregando modelo...")

#model = Qwen2VLForConditionalGeneration.from_pretrained(
    #"Qwen/Qwen2-VL-7B-Instruct"
#)

#print("Modelo carregado!")