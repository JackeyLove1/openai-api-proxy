# OpenAI API Proxy - Python Client

This README explains how to use the provided Python example script to connect to the OpenAI API proxy server and handle common errors like the 502 error you encountered.

## Error Analysis

The 502 error (Internal Server Error) you encountered typically indicates one of the following issues:

1. The proxy server is down or unreachable
2. The proxy server is encountering an internal error processing your request
3. Network connectivity issues between your client and the proxy server
4. Credential or configuration issues with the underlying LLM provider

## Setup Instructions

1. Install the required Python packages:

```bash
pip install openai
```

2. Configure the sample Python script:
   - Open `sample_openai_proxy.py`
   - Replace `your_proxy_api_key_here` with your actual API key for the proxy server
   - Update `PROXY_BASE_URL` to point to your deployed proxy URL (not the OpenAI URL)

3. Run the script:

```bash
python sample_openai_proxy.py
```

## Troubleshooting the 502 Error

If you encounter a 502 error when using the script:

1. **Check proxy server status**: Make sure your OpenAI API proxy server is running and accessible
2. **Verify API key**: Ensure your API_KEY for the proxy is correct 
3. **Check underlying API keys**: The proxy needs valid API keys for the underlying LLM services (OpenAI, Anthropic, etc.)
4. **Test connectivity**: Try a simple curl request to the proxy server:
   ```bash
   curl http://your-proxy-url/v1/models -H "Authorization: Bearer your_proxy_api_key"
   ```
5. **Check proxy server logs**: If you have access, check the logs on the proxy server
6. **Implement retry logic**: The sample includes retry logic for 502 errors (often transient)
7. **Try a different model**: Some models may be temporarily unavailable

## Advanced Configuration

The sample script includes:

- Error handling with retry logic
- Support for streaming responses
- Model listing capability
- Multiple request examples

You can modify the script to suit your specific needs, including changing the default model or adjusting retry parameters.

## Common Issues

1. **Incorrect base URL**: Make sure you're using the proxy URL, not the OpenAI URL
2. **Missing or invalid API key**: The proxy requires its own API key
3. **Model availability**: Not all models listed may be available (depends on your proxy setup)
4. **Rate limiting**: The proxy or underlying services may have rate limits
5. **Connection timeouts**: Adjust timeout settings for slower connections 