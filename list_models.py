import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyC7G9LAbM4eXHv2xhdu3NGN_DacRFuSmlA"
genai.configure(api_key=GOOGLE_API_KEY)

print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")
