# python-language-learning-app

1. Install Python: If you don't have Python installed on your machine, download and install it from https://www.python.org/downloads/. Make sure to check the "Add Python to PATH" option during installation.

--- Skip to step 4 if you don't want to connect to openAI api ---

---

2. Obtain a personal API key from OpenAI: Visit the following link to get your API key: https://platform.openai.com/account/api-keys

3. Install the OpenAI Python package: Open your terminal or command prompt and run the following command to install the OpenAI package:

sudo pip3 install openai

Set the OpenAI API key as an environment variable on your system:

For macOS or Linux: Run the following command in your terminal, replacing "your_api_key" with the actual API key:

export OPENAI_API_KEY="your_api_key"

For Windows: Run the following command in your Command Prompt or PowerShell, replacing "your_api_key" with the actual API key:

setx OPENAI_API_KEY "your_api_key"

Note that you might need to restart your terminal, command prompt, or IDE for the environment variable to take effect.

---

4. Clone the project: Clone the project repository from GitHub or download it as a ZIP file and extract it to a folder on your computer.

5. Open the project folder: Navigate to the folder where you've cloned or extracted the project files in your terminal or command prompt.

6. Superclass of BaseUser and two Subclasses: Premium and Regular. To begin, instantiate either a Premium or Regular object- it takes two arguments: the name of the user as a string e.g "John", and the data_directory variable.

7. Now the user has been created, instantiate Menu class with two arguments- the name of the player class e.g john. Second argument is the json file named 'my_words'. Commented out examples have been left in the program. These can be deleted as well ad the corresponding json files in the user_data folder.

8. Run the Python script: In your terminal or command prompt, run the following command to start the Python script:

python3 main.py
