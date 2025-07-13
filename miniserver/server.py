from flask import Flask, Response, stream_with_context
from ollama import chat
from ollama import ChatResponse
import requests
import time
from ollama import AsyncClient


app = Flask(__name__)

ollama_support=['llama3.2']

@app.route("/ollama/<model>", methods=['POST'])
def query_ollama(model):
	# Format: [{'role': ('user', 'assistant'), 'content': xxx}]
	post_messages = flask.request.form.get('messages')
	async def chat(messages, model):
		async for part in await AsyncClient().chat(model=model, messages=messages, stream=True):
			yield part['message']['content']

	return Response(stream_with_context(chat(post_messages, model), mimetype='application/json'))

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)

