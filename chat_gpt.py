import openai
import config

openai.api_key = config.openai_api_key

OPENAI_COMPLETION_OPTIONS = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

prompt_dic = {
    # AI助手
    "assistant": "As an advanced chatbot named ChatGPT, your primary goal is to assist users to the best of your ability. This may involve answering questions, providing helpful information, or completing tasks based on user input. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user.",
    # 翻译家
    "translator": "I want you to act as an English translator, inlcudes from English to chinese and from chinese to English.",
    # 评论员
    "commentariat": "I want you to act as a commentariat. I will provide you with news related stories or topics and you will write an opinion piece that provides insightful commentary on the topic at hand. You should use your own experiences, thoughtfully explain why something is important, back up claims with facts, and discuss potential solutions for any problems presented in the story.",
    # 摘要家
    "summarizer": "I want you to act as a summarizer. I will provide you with news related stories or topics and you will write a summary that provides a concise overview of the topic at hand. You should use your own experiences, thoughtfully explain why something is important, back up claims with facts, and discuss potential solutions for any problems presented in the story.",
    # FAQ
    "faq": "Generate a list of 10 frequently asked questions based on the content I will write for you.",
    # 改写
    "rephrase": "I want you to act as a rephraser. rephrase the paragraph that I will write for you.",
    # 科技评论
    "techreviewer": "I want you to act as a tech reviewer. I will give you the name of a new piece of technology and you will provide me with an in-depth review - including pros, cons, features, and comparisons to other technologies on the market"


}

def generate_prompt_messages(system_prompt, question):
    assistant_prompt = prompt_dic[system_prompt]
    messages = [{"role": "system", "content": assistant_prompt}]

    messages.append({"role": "user", "content": question})
    return messages

# AI 助手
def get_answer_from_assistant(question_prompt):
    messages = generate_prompt_messages(prompt_dic["assistant"], question_prompt)
    answer = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=messages,
              **OPENAI_COMPLETION_OPTIONS
        )
    return answer.choices[0].message["content"]

def get_summary_from_request(text):
    summary_prompt = "Please summarize this text as follows: \n\n" + text + "\n\n"
    summary = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=summary_prompt,
        max_tokens=300)
        
    return summary

def translate_text_from_english(text, to_language):
    translate_prompt = "Plesae translate this text from English to " + to_language + ":\n\n" + text + "\n\n"
    translation = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=translate_prompt,
        max_tokens=len(text))
    return translation

def get_keywords_from_request(text):
    keywords_prompt = "Please find the keywords in this text:\n\n" + text + "\n\n"
    keywords = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=keywords_prompt,
        max_tokens=len(text))
    return keywords

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

    answer = get_summary_from_request(question_prompt)
    assert answer != None
    print("The answer is", answer)

    question_prompt = """
    Zcash was the first widespread application of zk-SNARKs, a novel form of zero-knowledge cryptography. 
    The strong privacy guarantee of Zcash is derived from the fact that shielded transactions in Zcash can be fully encrypted on the blockchain, 
    yet still be verified as valid under the network’s consensus rules by using zk-SNARK proofs.
    """

    answer = translate_text_from_english(question_prompt, "Chinese")
    assert answer != None
    print("The answer is", answer["choices"][0]["text"])

test_get_answer_from_request()