# make sure you're logged in with `huggingface-cli login`
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("prompthero/midjourney-v4-diffusion")
pipe = pipe.to("cuda")

# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

#prompt = "mdjrny-v4 style, watercolour, people walking on moon"
prompt = "watercolour style, snow in a city view from streets with buildings and people walking"
prompt = "watercolour style, portrait of a lady with snow in the background"


# Results match those from the CPU device after the warmup pass.
image = pipe(prompt).images[0]
image.save("a.png")
