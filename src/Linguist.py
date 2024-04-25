import os
import streamlit as st
from decouple import config
from openai import OpenAI


def get_openai_api_key():
    api_key = config('OPENAI_API_KEY')
    if not api_key:
        api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        api_key = os.environ["OPENAI_API_KEY"]
    return api_key


CLIENT = OpenAI(api_key=get_openai_api_key())


class LangAgent:

    def translate_audio(self, audio_file):
        try:
            transcription = CLIENT.audio.translations.create(model="whisper-1", file=audio_file)
            if not transcription:
                raise Exception("Empty result !!!")
            return transcription.text
        except Exception as e:
            raise Exception("Failed to translate the audio file.")

    def translate_text(self, text):
        if not text:
            return None

        system_prompt = """
        You are a translator. 
        The user will provide you a text.
        If the majority of the provided text is not in English language, translate the text in English and fix grammatical issues.
        """
        max_tokens = 2000
        temperature = 1

        try:
            print(">>>GPT System", system_prompt)
            print(">>>GPT Query", text)
            completion = CLIENT.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            result = completion.choices[0].message.content
            print(">>>GPT Response", result)
            return result
        except Exception as e:
            raise Exception(f'GPTQuery Error: {str(e)}')

    def fix_grammar(self, text):
        system_prompt = """
        Act as an English Grammar expert. 
        Rewrite the text fixing grammatical issues.
        """
        max_tokens = 2000
        temperature = 1

        try:
            print(">>>GPT System", system_prompt)
            print(">>>GPT Query", text)
            completion = CLIENT.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            result = completion.choices[0].message.content
            print(">>>GPT Response", result)
            return result
        except Exception as e:
            raise Exception(f'GPTQuery Error: {str(e)}')

    def answer(self, query, context):
        system_prompt = f"""
        Act as an excellent answering machine.
        You'll be given a query and a context.
        Answer the query from the provided context. 
        Only answer within the provided context.
        
        <Context>
        {context}
        </Context>
        """
        max_tokens = 800
        temperature = 1

        try:
            print(">>>GPT System", system_prompt)
            print(">>>GPT Context", context)
            print(">>>GPT Query", query)
            completion = CLIENT.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            result = completion.choices[0].message.content
            print(">>>GPT Response", result)
            return result
        except Exception as e:
            raise Exception(f'GPTQuery Error: {str(e)}')

