from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction="I want you to act as an API, i will give you a description of a song or album, and you have to give me an Array of Strings as the names of Songs that exist in spotify, add the name of the artist in the string too, avoid using puntuation, like \"-\" \",\". Use plain espaces separatin the words, use symbols only if the name requires it, just like if you were seaching the song in spotify, without typing weird symbols etc.\n\nThe answer you give has to be only and only an array of Strings, because later ill do response.json() so the format has to be valid for parsing to json, you cant send any other information, like context, details, etc. \n\nIf i ask you for an album you have to give me the names of the songs in that album, if i ask for a song by giving a description of the song, then you have to give me a list of names of songs that could fit with that description. I could ask you about songs by giving you parts of the lyrics, so be sure to think of any song that could contian the lyrics, focus on giving a proper answer to the description, also give short names, long names may produce spotify to show a result that is non related to the given name. If you are not sure of the answer give multiple names, its ok, \n\nBut dont answer with text formatted like markdown, like using ```json etc, dont. Answer as plain text but in the correct format of a json\nIf my question has nothing to do with sugesting songs, then answer with names of songs that could answer that question.",
)

def wonder_songs(description: str):
  chat_session = model.start_chat()
  response = chat_session.send_message(description)
  
  print(response.text)
  response_json = json.loads(response.text)
  
  
  return response_json










