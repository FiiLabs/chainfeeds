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
    "translater": "I want you to act as an English translator, inlcudes from English to chinese and from chinese to English.",
    # 评论员
    "commentariat": "I want you to act as a commentariat. I will provide you with news  or topics and you will write an opinion piece that provides insightful commentary on the topic at hand. You should use your own experiences, thoughtfully explain why something is important, back up claims with facts, and discuss potential solutions for any problems presented in the story.",
    # 摘要家
    "summarizer": "I want you to act as a summarizer. I will provide you with news related stories or topics and you will write a summary that provides a concise overview of the topic at hand. You should use your own experiences, thoughtfully explain why something is important, back up claims with facts, and discuss potential solutions for any problems presented in the story.",
    # FAQ
    "faq": "Generate a list of 10 frequently asked questions based on the content I will write for you.",
    # 改写
    "rephrase": "I want you to act as a rephraser. rephrase the paragraph that I will write for you.",
    # 科技评论
    "techreviewer": "I want you to act as a tech reviewer. I will give you a tech article and you will provide me with an in-depth review - including pros, cons, features, and comparisons to other technologies on the market"


}

def generate_prompt_messages(system_prompt, question):
    assistant_prompt = prompt_dic[system_prompt]
    messages = [{"role": "system", "content": assistant_prompt}]

    messages.append({"role": "user", "content": question})
    return messages

def get_answer_from_request(messages):
    answer = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=messages,
              **OPENAI_COMPLETION_OPTIONS
        )
    return answer.choices[0].message["content"]

# AI助手
def get_answer_from_assistant(message):
    messages = generate_prompt_messages(prompt_dic["assistant"], message)
    return get_answer_from_request(messages)

# 翻译家
def get_answer_from_translater(message):
    messages = generate_prompt_messages(prompt_dic["translater"], message)
    return get_answer_from_request(messages)

# 评论员
def get_answer_from_commentariat(message):
    messages = generate_prompt_messages(prompt_dic["commentariat"], message)
    return get_answer_from_request(messages)

# 摘要家
def get_answer_from_summarizer(message):
    messages = generate_prompt_messages(prompt_dic["summarizer"], message)
    return get_answer_from_request(messages)

# FAQ
def get_answer_from_faq(message):
    messages = generate_prompt_messages(prompt_dic["faq"], message)
    return get_answer_from_request(messages)

# 改写段落
def get_answer_from_rephrase(message):
    messages = generate_prompt_messages(prompt_dic["rephrase"], message)
    return get_answer_from_request(messages)

# 科技评论
def get_answer_from_techreviewer(message):
    messages = generate_prompt_messages(prompt_dic["techreviewer"], message)
    return get_answer_from_request(messages)

# write a unit test for this function
def test_get_answer_from_request():
   pass

test_get_answer_from_request()