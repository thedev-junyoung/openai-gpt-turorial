# OpenAI GPT API Client

This library provides an easy-to-use Python interface for interacting with OpenAI's GPT models, including both the Assistant API and the Completion endpoint.

## Features

- Interactive GPT with Assistant
- gpt request with Completions api
- Cost calculation for api requests and responses from openai
## Getting Started
1. Clone the Repository: Clone this repository to your local machine:
```shell
git clone https://github.com/thedev-junyoung/GoogleDrivePyManager.git
```

2. To get started with this library, you'll need to install it via `pip` and set up your OpenAI API key.
```bash
pip install openai python-dotenv
```
3. create a .env file at the root of your project and include your OpenAI API key:

```bash
OPENAI_API_KEY='your-api-key-here'
```


## Example Usage

This library supports both text completions using the Completion API and structured conversations with the Assistant API. Below are examples of how to use each feature.

### Using the Completion API for Text Generation

To generate text completions, such as answering a trivia question, use the following code:

```python
from dotenv import load_dotenv
from openai_api_client import OpenAICompletion  # Ensure you have this module in your project
import os

if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()
    
    # Retrieve your OpenAI API key from the .env file
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Initialize the completion service with the specified model
    service = OpenAICompletion(model_name="gpt-3.5-turbo", open_ai_key=OPENAI_API_KEY)
    
    # Provide the system prompt and user input
    system_prompt = "You are a helpful assistant designed to output JSON."
    user_input = "Who won the world series in 2020?"
    
    # Call the generate function to get the result
    result = service.generate(system_prompt, user_input)
    
    # Print the resulting text completion
    print(result)
```
### Using the Completion API

The Completion API can be used to generate text completions for a variety of tasks.

```python
from dotenv import load_dotenv
from legal_document_service import OpenAICompletion
import os

if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()
    # Get API key from the .env file
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OpenAICompletion
    # Initialize the service with the chosen model
    service = OpenAICompletion(model_name="gpt-3.5-turbo", open_ai_key=OPENAI_API_KEY)
    
    # System prompt and user input for generating a legal document
    system_prompt = "You are a helpful assistant designed to output JSON."
    user_input = "Who won the world series in 2020?"
    
    # Generate the legal document
    result = service.generate(system_prompt, user_input)
    
    # Print the result
    print(result)

```


## References
- [Text generation with JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode)
- [Chat completions API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api)
- [Assistants overview](https://platform.openai.com/docs/assistants/overview)
- [OpenAI Pricing](https://openai.com/pricing)
