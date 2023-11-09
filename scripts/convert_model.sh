model_path=models/vicuna-7b-v1.5/
# you should select proper model_type for different model
# llama,llama2, vicuna,qwen....
#python3 -m lmdeploy.serve.turbomind.deploy llama ${model_path} hf \
python3 -m lmdeploy.serve.turbomind.deploy vicuna ${model_path} hf \
    --tokenizer_path ${model_path}/tokenizer.model --tp 1
