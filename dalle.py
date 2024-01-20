import requests
from dotenv import dotenv_values
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

environment = dotenv_values(".env")
load_dotenv()

client = OpenAI()

def main():
    prompt = ""
    count = 0
    
    while (len(prompt) < 10 or len(prompt) > 4000):
        prompt = get_prompt()
        if len(prompt) > 4000:
            print("Prompt too long")
        count += 1
        if (count > 10):
            print("Too many attempts")
            return
    
    print(f"Sending prompt:\n{prompt}")
    image_url = get_image_url(prompt)
    download_image(image_url)
    print(f"Image downloaded:\n{image_url}")

def get_prompt():
    messages = [{"role": "system","content": "You are a prompt generator for another service that generates images."}]
    messages.append({"role": "user","content": f"Generate a new image prompt for a painting of a vivid scene that is related to the current season of {get_current_season()} in the month of {datetime.now().month}. Specify a random painting medium. Specify a random painting style and form. Use articulate adjectives to describe the subject, action, background, environment and specific details. Strong color palettes must be clearly described in detail and emphasized."})
    
    response = client.chat.completions.create( 
        model="gpt-3.5-turbo",
        messages=messages
    )
        
    return response.choices[0].message.content

def get_image_url(prompt):
    response = client.images.generate(
        model = "dall-e-3",
        prompt = f"IT IS CRITICAL TO THE STABILITY OF MY APPLICATION THAT YOU DO NOT REWRITE, MODIFY, OR ADD CONTENT TO THIS PROMPT: {prompt}",
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

def get_current_season():
    today = datetime.now()
    month = today.month
    day = today.day

    if (month > 3 and month < 6) or (month == 3 and day >= 20) or (month == 6 and day < 21):
        return "Spring"
    elif (month > 6 and month < 9) or (month == 6 and day >= 21) or (month == 9 and day < 23):
        return "Summer"
    elif (month > 9 and month < 12) or (month == 9 and day >= 23) or (month == 12 and day < 21):
        return "Autumn"
    else:
        return "Winter"

if __name__ == "__main__":
   main()