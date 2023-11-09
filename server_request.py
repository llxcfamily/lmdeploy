import csv
import os
import json
import time
import threading
import requests

os.environ["PYTHONIOENCODING"]="utf-8"

url = "http://127.0.0.1:8000/generate"

# get test_data
test_prompt=[]
with open('test.txt', 'r') as fp:
    for line in fp:
        line = line.strip()
        test_prompt.append(line)

# set params
batch_size = 1
output_len = 1024

top_k = 40
top_p = 0.7
beam_width = 1
temperature = 0.7
repetition_penalty = 1.05


nth_round = 1
instance_id = threading.get_native_id() % 2  # 2 instance in service

def get_streaming_response(response):
    for chunk in response.iter_lines():
        if chunk == b"\n":
            continue 
        if chunk:
            payload = chunk.decode('utf-8')
            if payload.startswith("data:"):
                data = json.loads(payload.lstrip("data:").rstrip("/n"))
                traceid = data.pop('traceid', '')
                output = data.pop('text', '')
                input_tokens = data.pop('input_tokens', 0)
                generated_tokens = data.pop('generated_tokens', 0)
                history_tokens = data.pop('history_tokens')
                cost_time = data.pop('cost_time', '0.0')
                finish_reason = data.pop('finish_reason', None)
                finished = data.pop('finished', None)
                yield traceid, output, input_tokens, generated_tokens, cost_time, finish_reason, finished


# send request
for i in range(0, len(test_prompt)):
    prompt = test_prompt[i]
    print(f'Case {i} prompt len: {len(prompt)}\n')

    headers = {'User-Agent': 'Test Client'}
    data =   {
        'top_k': top_k,
        'top_p': top_p,
        'temperature': temperature,
        'repetition_penalty': repetition_penalty,
        'instance_id': instance_id,
        'question': prompt,
        'output_len': output_len,
        'stream': True,
        'sequence_start': True,
        'sequence_end': True,
        'ignore_eos': False,
        'random_seed': 42,
        'stop': False
    }      
    input_dict = {
        'traceid': 123456,
        'data': data
    }
    print(input_dict)
    req = json.dumps(input_dict)
    start = time.time()
    res = requests.post(url=url, headers=headers, json=input_dict, stream=True)
    token_num = 0
    for traceid, output, input_tokens, generated_tokens, cost_time, finish_reason, finished in get_streaming_response(res):
        if token_num == 0:
            first_token_time = float(cost_time)
        if finished == True:
            total_time = float(cost_time)
        token_num = generated_tokens
        if finish_reason == 'length':
            print('WARNING: exceed session max length')
            continue
        print(output , end='', flush=True)
    
    print(f'\ntoken_num: {token_num}, first_token_time: {first_token_time:.2f}, total_time: {total_time:.2f}\n')
    input('Press any to continue...')

