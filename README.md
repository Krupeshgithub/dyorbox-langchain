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

# Ask Question API
The request body includes two parameters: "question" for the question to be asked, and "user_id" for maintaining session uniqueness. Ensure a unique user ID is provided for each session.
### Ask Question
```bash
curl -i -XPOST "http://localhost:8000/ask" \
--header "Content-Type: application/json" \
--header "Authorization: df076c44-1018-4888-b3a7-6cd4d821e322" \
--data '{
  "question": "How can I contact the Calette Reef Club?",
  "user_id": "001"
}'
```
### Response
```bash
{
  "answer": "You can contact the Calette Reef Club by emailing info@calettereefclub.com or by visiting their entrance at Presidiana touristic harbour in Cefalù."
}
```
# Clear Session API
It will reset the session for a specific user, removing any previously stored context and erasing the conversation history associated with that particular user ID.
### Ask Question
```bash
curl -i -XPOST "http://localhost:8000/clear-user-session" \
--header "Content-Type: application/json" \
--data '{
  "user_id": "001"
}'
```
### Response
```bash
{
  "message": "success"
}
```
