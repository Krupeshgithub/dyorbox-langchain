# Langchain-LLM

LangChain provides AI developers with tools to connect language models with external data sources. It is open-source and supported by an active community.

# Prerequisites:
 1. Python
 2. Basic understanding about langchain

# Python libraries included are:

 1. Langchain
 2. OpenAI


# Follow Below steps to run game.
 1. For run project
    ```bash
    source run.sh "Your OpenAiKey" "ChatHistoryCount"
    ```
> - Note: Please note that `ChatHistoryCount` is the user's previous records. Please note that the output will be given with your previous and current questions. For example, if `ChatHistoryCount = 3` your `last 3 questions + current questions = answer`. After the three questions, your `current question = answer`.

## For integrate:
>- Note: We have driver code available if you wish to integrate this script with your own. Please take the actions listed below.

```bash
from util import LangChainAPI

resp = LangChainAPI(
  user_id="User's ID",
  question="User's Question"
)
```
