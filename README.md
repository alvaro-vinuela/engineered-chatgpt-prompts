# engineered-chatgpt-prompts
Create elaborated chatgtp prompts using a specified goal input text is processed by the chatgpt model

## Installation
`python3 -m pip install -r requirements.txt`

## Configuration
Set your open api key on your .env file with the following format:
```
OPENAI_API_KEY=<your-key>
OPENAI_ORGANIZATION=<your-organizatio-or-personal-id>
```

## Links:
- [Where do I find openai api key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
## Usage
Launch application in graphical mode with:

`python engineered_chatgpt_prompts.py`

To launch application on batch mode over a directory or file, check help:

`python engineered_chatgpt_prompts.py -h`

output:
```
usage: engineered_chatgpt_prompts.py [-h] [-d DIR] [-f FILE] [-g GOAL]

Launch engineered chatgtp prompts tool on graphical or command line mode.

Example processing a directory in batch mode:
  python engineered_chatgtp_prompts.py --directory="/path/to/directory" --goal="/path/to/goal"

Example processing a file in batch mode:
  python engineered_chatgtp_prompts.py --file="/path/to/file" --goal="${PWD}/goals/general/summarize.txt"

Example Launching it on graphical mode:
  python engineered_chatgtp_prompts.py 

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     dir to process
  -f FILE, --file FILE  file to process
  -g GOAL, --goal GOAL  goal to do on directory
```
