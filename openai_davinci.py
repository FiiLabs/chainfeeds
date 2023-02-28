import openai

API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

openai.api_key = API_KEY

def get_answer_from_request(question_prompt):
    answer = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question_prompt,
        max_tokens=300)
        
    return answer

