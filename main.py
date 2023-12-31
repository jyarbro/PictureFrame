from dotenv import dotenv_values
import requests
import time
import leonardoaisdk
from leonardoaisdk.models import operations
import openai

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
    
    generation_id = get_generation_id(prompt)
    image_url = get_image_url(generation_id)
    download_image(image_url)
    delete_image(generation_id)

def get_prompt():
    openai.api_key = environment["OPENAI_API_KEY"]
    
    messages = [{"role": "system","content": environment["SYSTEM_PROMPT"]}]
    messages.append({"role": "user","content":  environment["USER_PROMPT"]})
    
    chat = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo",
        messages=messages
    )
        
    return chat.choices[0].message["content"]

def get_generation_id(prompt):
    server = leonardoaisdk.LeonardoAiSDK(
        bearer_auth=environment["LEONARDO_API_KEY"],
    )

    request = operations.CreateGenerationRequestBody(
        num_images=1,
        width=1224,
        height=768,
        prompt=prompt
    )

    response = server.generation.create_generation(request)

    if response.create_generation_200_application_json_object is not None:
        return response.create_generation_200_application_json_object.sd_generation_job.generation_id
    else:
        print(response.raw_response.text)

def get_image_url(generation_id):
    server = leonardoaisdk.LeonardoAiSDK(
        bearer_auth=environment["LEONARDO_API_KEY"],
    )

    image_url = ""
    attempts = 0
    
    while (image_url == "" and attempts < 10):
        attempts += 1
        time.sleep(10)
        response = server.generation.get_generation_by_id(generation_id)
        if response.get_generation_by_id_200_application_json_object is not None:
            if len(response.get_generation_by_id_200_application_json_object.generations_by_pk.generated_images) > 0:
                image_url = response.get_generation_by_id_200_application_json_object.generations_by_pk.generated_images[0].url
            
    return image_url

def download_image(image_url):
    if (image_url != ""):
        image_data = requests.get(image_url).content
        
        with open('output.jpg', 'wb') as handler:
            handler.write(image_data)

def delete_image(generation_id):
    server = leonardoaisdk.LeonardoAiSDK(
        bearer_auth=environment["LEONARDO_API_KEY"],
    )
    
    server.generation.delete_generation_by_id(generation_id)

if __name__ == "__main__":
   main()