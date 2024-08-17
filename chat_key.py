import random
import os
from http import HTTPStatus
from dashscope import Generation
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")



def chat_keyword(query):
    messages = [
        {'role': 'user', 
         'content': f'下面我将给你一个句子，提取该句子的关键词。\n 句子：{query}'}]
    responses = Generation.call(
        'qwen2-7b-instruct',
        messages=messages,
        seed=1234,  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=False , # get streaming output incrementally
    )   #qwen1.5-14b-chat/qwen2-7b-instruct
    full_content = []
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            full_content.append(response.output.choices[0]['message']['content'])
            #print(response.output.choices[0]['message']['content'])
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return 'False'

    return full_content[-1]

if __name__ == '__main__':
    quary = 'The hybrid five-level single-phase rectifier proposed in the paper utilizes a quadtree data structure for efficient point cloud representation and compression.。'
    
    print(chat_keyword(quary))