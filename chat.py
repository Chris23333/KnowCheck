import random
import os
from http import HTTPStatus
from dashscope import Generation
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

#dashscope.api_key_file_path = "algorithm\key.txt"
#下面给定的QUERY中可能会包含隐藏的不正确信息，请仔细比对给定的Known_Information，判断QUERY的正确性。请注意你只需要返回一个单词:True 或者 False。我再说一遍要求，请根据Known_Information的内容判断QUERY是否正确，注意你只需要返回一个单词:True 或者 False。\n QUERY: “ {query}”。\n Known_Information:“{example}”.

def chat(query,example):
    messages = [
        {'role': 'user', 
         'content': f'背景材料:“{example}”.\n 请根据以上背景材料，判断QUERY中的陈述是否正确。 QUERY: “ {query}”。\n 回答选项：True 或者 False \n 注意你只需要返回一个单词:True 或者 False。'}]
    responses = Generation.call(
        'qwen2-7b-instruct',
        messages=messages,
        seed=1234,  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=True,
        output_in_full=False  # get streaming output incrementally
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

# if __name__ == '__main__':
#     quary = '利用可编程技术改进设备接受逻辑，可以降低数据排队时延'
#     example = 'A multipath low latency forwarding scheduling algorithm for computing power networks is studied, which dynamically updates the path value to generate path forwarding decisions based on network state changes. Within a certain confidence probability, multiple backup transmissions are carried out in the form of multiple redundant contracts to reduce path propagation delay. In addition, a rank and queue mapping algorithm is proposed, which uses network programmable technology to improve the device forwarding logic and uses a limited number of strict priority queues to ensure that packets are approximately queued according to the rank, reducing the data queue delay. Simu⁃ lation results show that the proposed method can reduce data transmission delay and jitter, and provide stable throughput for computing net⁃ work services.'
#     print(chat(quary,example))