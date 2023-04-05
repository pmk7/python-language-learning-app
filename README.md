# language-learning-app

To make use of the sentence generator, follow this link to get a personal API key from openai: https://platform.openai.com/account/api-keys

Next, in the command line run 'pip install openai'
On mac, run export OPENAI_API_KEY="your_api_key"

Now, the OpenAI API key is set as an environment variable on your macOS system. You can access it in your Python script using: import os
api_key = os.getenv("OPENAI_API_KEY")
