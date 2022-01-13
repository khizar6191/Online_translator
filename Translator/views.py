from django.shortcuts import render
import requests
import uuid
import os
import json
from pathlib import Path
import azure.cognitiveservices.speech as speechsdk
BASE_DIR = Path(__file__).resolve().parent.parent

Auth=json.load(open(BASE_DIR/'Auth.json'))

def Translator(request):
	if request.method == 'POST':
		original_text = request.POST['text']
		target_language = request.POST['language']
		key = Auth['KEY']
		endpoint = Auth['ENDPOINT']
		location = Auth['LOCATION']
		path = '/translate?api-version=3.0'

		target_language_parameter = '&to=' + target_language


		# Create the full URL
		constructed_url = endpoint + path + target_language_parameter

		# subscription key
		headers = {
			'Ocp-Apim-Subscription-Key': key,
			'Ocp-Apim-Subscription-Region': location,
			'Content-type': 'application/json',
			'X-ClientTraceId': str(uuid.uuid4())
				}
		body = [{'text': original_text}]

		# Make the call using post
		translator_request = requests.post(constructed_url, headers=headers, json=body)

		# Retrieve the JSON response
		translator_response = translator_request.json()

		# Retrieve the translation
		translated_text = translator_response[0]['translations'][0]['text']

		# Call render template, passing the translated text,
		# original text, and target language to the template
		dict ={
			'translated_text':translated_text,
			'original_text':original_text,
			'target_language':target_language
		}
		return render(request,'result.html',context=dict)

	return render(request,'index.html')
def index(request):
	return render(request,'index.html')