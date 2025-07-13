from quart import Quart, Response, request, stream_with_context
import asyncio
import json
from ollama import AsyncClient

app = Quart(__name__)

@app.route("/ollama/<model>", methods=['POST'])
async def query_ollama(model): #Make the view function async
    if not (data := await request.data): # Await and store in a variable
        return "No data provided", 400

    try:
        post_messages = json.loads(data.decode('utf-8')) # Use the stored data
    except json.JSONDecodeError:
        return "Invalid JSON data", 400

    @stream_with_context
    async def chat_stream(messages, model):
        try:
            async for part in await AsyncClient().chat(model=model, messages=messages, stream=True):
                yield part["message"]["content"]  # Yield the data directly
        except Exception as e:
            yield {"error": str(e)}  # Yield an error object

    return chat_stream(post_messages, model)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
