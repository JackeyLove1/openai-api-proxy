import os
import openai
from openai import OpenAI
import sys

# Configure your API keys and endpoints
PROXY_API_KEY = "your_proxy_api_key_here"
PROXY_BASE_URL = "http://localhost:8787/v1"  # Change to your deployed proxy URL

# Initialize the OpenAI client with the proxy
client = OpenAI(
    api_key=PROXY_API_KEY,
    base_url=PROXY_BASE_URL,
)


def list_models():
    """List all available models through the proxy"""
    try:
        models = client.models.list()
        print("Available models:")
        for model in models.data:
            print(f" - {model.id} (owned by: {model.owned_by})")
        return models.data
    except Exception as e:
        print(f"Error listing models: {str(e)}", file=sys.stderr)
        return []


def generate_completion(model="gpt-4o-mini", messages=None, max_retries=3):
    """Generate a completion using the specified model"""
    if messages is None:
        messages = [{"role": "user", "content": "Hello, world!"}]

    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"Sending request to model: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
            )
            return response
        except openai.InternalServerError as e:
            retry_count += 1
            print(
                f"Server error (502): Attempt {retry_count}/{max_retries}",
                file=sys.stderr,
            )
            if retry_count >= max_retries:
                print(f"Failed after {max_retries} attempts: {str(e)}", file=sys.stderr)
                raise
        except Exception as e:
            print(f"Error generating completion: {str(e)}", file=sys.stderr)
            raise


def generate_stream(model="gpt-4o-mini", messages=None):
    """Generate a streaming completion using the specified model"""
    if messages is None:
        messages = [
            {
                "role": "user",
                "content": "Tell me a short story about a robot learning to paint.",
            }
        ]

    try:
        print(f"Streaming response from model: {model}")
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()  # Add a newline at the end

    except Exception as e:
        print(f"Error in streaming: {str(e)}", file=sys.stderr)


def main():
    # Uncomment to set environment variables if not set elsewhere
    # os.environ["OPENAI_API_KEY"] = "your_actual_openai_key_if_needed"

    print("OpenAI API Proxy Example")
    print("-----------------------")

    # List available models
    models = list_models()
    if not models:
        print("No models available or couldn't retrieve models list.")
        return

    # Choose a model to use (preferably something that exists in your proxy)
    selected_model = "gpt-4o-mini"  # Change to your preferred model

    # Generate a completion
    try:
        messages = [
            {"role": "user", "content": "What are the benefits of API proxies?"}
        ]
        response = generate_completion(selected_model, messages)

        print("\nCompletion Response:")
        print(f"Model: {response.model}")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Failed to generate completion: {str(e)}")

    # Generate a streaming response
    print("\nStreaming Response:")
    try:
        messages = [{"role": "user", "content": "Write a haiku about technology."}]
        generate_stream(selected_model, messages)
    except Exception as e:
        print(f"Failed to generate streaming response: {str(e)}")


if __name__ == "__main__":
    main()
