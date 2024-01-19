import requests
from dotenv import dotenv_values
from openai import OpenAI

client = OpenAI()
environment = dotenv_values(".env")

def main():
    prompt = ""
    count = 0
    
    while (len(prompt) < 10 or len(prompt) > 999):
        prompt = get_prompt()
        if len(prompt) > 999:
            print("Prompt too long")
        count += 1
        if (count > 10):
            print("Too many attempts")
            return
    
    image_url = get_image_url(prompt)
    download_image(image_url)

def get_prompt():
    messages = [{"role": "system","content": environment["SYSTEM_PROMPT"]}]
    messages.append({"role": "user","content":  environment["USER_PROMPT"]})
    
    response = client.chat.completions.create( 
        model="gpt-3.5-turbo",
        messages=messages
    )
        
    return response.choices[0].message.content

def get_image_url(prompt):
    prompt = environment["IMAGE_PROMPT"] + " " + prompt
    
    response = client.images.generate(
        model = "dall-e-3",
        prompt = prompt,
        size = "1792x1024",
        quality = "hd",
        n=1,
    )
    
    return response.data[0].url

def download_image(image_url):
    if (image_url != ""):
        image_data = requests.get(image_url).content
        
        with open('output.jpg', 'wb') as handler:
            handler.write(image_data)

if __name__ == "__main__":
   main()