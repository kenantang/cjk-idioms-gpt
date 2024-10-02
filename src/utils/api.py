import os

import deepl
from google.cloud import translate
from openai import OpenAI

client = OpenAI()

def get_response_gpt(prompt, model, seed=0, temperature=1.0, single_turn=True):
    '''
    prompt: either a string or a list as the input
    model: either gpt-3.5-turbo or gpt-4-0125-preview
    seed: requires further official support from OpenAI
    temperature: controls randomness in generation
    single_turn: whether the dialog is single-turn or not
    '''

    if single_turn:
        response = client.chat.completions.create(
            model = model,
            messages = [{'role': 'user', 'content': prompt}],
            seed = seed,
            temperature=temperature
        )
    else:
        response = client.chat.completions.create(
            model = model,
            messages = prompt,
            seed = seed,
            temperature=temperature
        )

    return response.choices[0].message.content

GOOGLE_PROJECT_ID = os.environ['GOOGLE_PROJECT_ID']

# copied and modified from https://cloud.google.com/translate/docs/advanced/translating-text-v3#translating_input_strings
# Initialize Translation client
def get_translation_google(
    text: str = "YOUR_TEXT_TO_TRANSLATE", project_id: str = GOOGLE_PROJECT_ID, source_language_code: str = 'zh'
) -> translate.TranslationServiceClient:
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from a given language to english
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats

    # to resolve TypeError: TranslationServiceClient.translate_text() got an unexpected keyword argument 'request'
    # modified based on https://stackoverflow.com/questions/77476982/google-translate-api-typeerror-translationserviceclient-translate-text-got-an
    request = {
        "parent": parent,
        "contents": [text],
        "mime_type": "text/plain",  # mime types: text/plain, text/html
        "source_language_code": source_language_code,
        "target_language_code": "en",
    }

    response = client.translate_text(**request)

    return response.translations[0].translated_text

auth_key = os.environ['DEEPL_API_KEY']
translator = deepl.Translator(auth_key)

def get_translation_deepl(text, source_lang):
    result = translator.translate_text(text, source_lang=source_lang, target_lang='EN-US')
    return result.text