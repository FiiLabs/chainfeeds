import openai
import os

API_KEY = "sk-cshdoUShCYzJFnV4AzNvb3qT3BlbkFJziibz7eA57Xv1q0bzGvr"

openai.api_key = os.getenv("OPENAI_API_KEY", API_KEY)

def get_answer_from_request(question_prompt):
    answer = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question_prompt,
        max_tokens=300)
        
    return answer

# write a unit test for this function
def test_get_answer_from_request():
    question_prompt = "What is the answer to life, the universe, and everything?"
    answer = get_answer_from_request(question_prompt)
    assert answer != None
    print("The answer is", answer)

    question_prompt = """
    Summarize this for a second-grade student:

    Jupiter is the fifth planet from the Sun and the largest in the Solar System. 
    It is a gas giant with a mass one-thousandth that of the Sun, 
    but two-and-a-half times that of all the other planets in the Solar System combined. 
    Jupiter is one of the brightest objects visible to the naked eye in the night sky, 
    and has been known to ancient civilizations since before recorded history. 
    It is named after the Roman god Jupiter.[19] When viewed from Earth, 
    Jupiter can be bright enough for its reflected light to cast visible shadows,
    [20] and is on average the third-brightest natural object in the night sky after the Moon and Venus.
    """

    answer = get_answer_from_request(question_prompt)
    assert answer != None
    print("The answer is", answer)

test_get_answer_from_request()