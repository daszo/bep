from transformers import MT5ForConditionalGeneration

print("Downloading standard pytorch_model.bin...")
model = MT5ForConditionalGeneration.from_pretrained("google/mt5-base")

# This flag forces it to save as pytorch_model.bin instead of safetensors
model.save_pretrained("./mt5-bin-local", safe_serialization=False)

print("Done! check ./mt5-bin-local folder.")
