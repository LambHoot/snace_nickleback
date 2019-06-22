# snace_nickleback

Here are any notes regarding setting this up and streaming it.

pip install python-twitter
pip install textgenrnn
https://www.tensorflow.org/install/pip
.\venv\Scripts\activate
deactivate  # don't exit until you're done using TensorFlow

# Streaming
To get vs code to be streamable by obs, it must be launched without hardware acceleration through windows powershell:
> code --disable-gpu

For data security reasons it may be desired to hide certain files from the explorer and search in vs code. This can be done using the exclude settings.
File > Preferences > Settings
search for "Files: Exclude" and add a pattern to hide the files you want.
For example in my project, I've decided that any files with sensitive information like api keys, I will call .acecfg files. This rule excludes them all from vs code:
> **/*.acecfg

# Config
The application expects a config file with twitter keys to be located in the config folder
<keys.acecfg>
This file should contain only 4 lines with the keys provided by https://developer.twitter.com/en/apps/ and should have them in this order
keys.acecfg {
    API_KEY
    API_SECRET_KEY
    ACCESS_TOKEN
    ACCESS_TOKEN_SECRET
}

# to find location of a module
help('textgenrnn')

# to run from windows powershell
\GitHub2\snace_nickleback> python .\app\TwitterBot.py

