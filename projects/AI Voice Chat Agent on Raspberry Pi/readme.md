# AI Voice Chat Agent on Raspberry Pi

A project exploring the capabilities of the Raspberry Pi by building an interactive voice chat agent. Users can speak to the bot via a microphone, and it responds audibly using a local AI model (Ollama with Gemma 3). A simple graphical user interface is included for a more interactive experience.

**Key Features:**

* Voice input using microphone.
* Integration with a local AI model (Gemma 3 via Ollama).
* Text-to-speech output.
* Basic graphical user interface with chat history.

**Using the program:**

* Create a virtual environment for all the necessary libraries in the same folder as the python files
* Make sure to install Ollama and Gemma 3:1b
* Run "python3 main.py" in the terminal

(If the AI model doesn't give an answer, make sure Ollama is running in the background with "ollama serve")

**Note:** Speech recognition and TTS currently relies on an internet connection.

©️ Andreh Samaan
