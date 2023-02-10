from diffusers import DiffusionPipeline

def generate_image(prompt):
    pipe = DiffusionPipeline.from_pretrained("prompthero/midjourney-v4-diffusion")
    pipe = pipe.to("cuda")
    # Recommende if your computer has < 64 GB of RAM
    pipe.enable_attention_slicing()
    # Results match those from the CPU device after the warmup pass.
    image = pipe(prompt).images[0]
    image.save("a.png")

def main():
    #prompt = "mdjrny-v4 style, watercolour, people walking on moon"
    prompt = "watercolour style, snow in a city view from streets with buildings and people walking"
    prompt = "watercolour style, portrait of a lady with snow in the background"
    generate_image(prompt)

if __name__== "__main__":
    main()