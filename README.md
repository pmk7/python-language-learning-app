# language-learning-app

To utilize the sentence generator with OpenAI, follow these steps:

1. Obtain a personal API key from OpenAI by visiting the following link: https://platform.openai.com/account/api-keys
2. Install the OpenAI Python package by running the following command in your terminal or command prompt:

'pip install openai''

3. Set the OpenAI API key as an environment variable on your system:
   For macOS or Linux: Run the following command in your terminal, replacing "your_api_key" with the actual API key:

export OPENAI_API_KEY="your_api_key"
For Windows: Run the following command in your Command Prompt or PowerShell, replacing "your_api_key" with the actual API key:

setx OPENAI_API_KEY "your_api_key"
Note that you might need to restart your terminal, command prompt, or IDE for the environment variable to take effect.

4. In your Python script, access the OpenAI API key using the following code:
   python

api_key = os.getenv("OPENAI_API_KEY")

Now you have successfully set up the OpenAI API key and can access it in your Python script. With this configuration, you can start using the sentence generator with the OpenAI package.
