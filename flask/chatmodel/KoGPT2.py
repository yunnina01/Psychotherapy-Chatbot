import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# KoGPT2 토크나이저 및 모델 로드
model_name = "skt/kogpt2-base-v2"
tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# 특수 토큰 설정
pad_tokens_dict = {'pad_token': '<pad>'}

num_added_toks = tokenizer.add_special_tokens(pad_tokens_dict)
model.resize_token_embeddings(len(tokenizer))

# 모델 정의
class KoGPT2ChatModel(nn.Module):
    def __init__(self, kogpt2_model):
        super(KoGPT2ChatModel, self).__init__()
        self.kogpt2 = kogpt2_model
    
    def forward(self, input_ids, attention_mask=None):
        outputs = self.kogpt2(input_ids=input_ids, attention_mask=attention_mask)

        logits = outputs.logits if isinstance(outputs, dict) else outputs[0]

        return logits

    def generate(self, input_ids, **kwargs):
        return self.kogpt2.generate(input_ids, **kwargs)

# 답변 생성
def generate_response(question, model, tokenizer):
    model.eval()
    with torch.no_grad():
        device = next(model.parameters()).device    # 디바이스 설정 초기화
        input_ids = tokenizer.encode(tokenizer.bos_token + question + tokenizer.eos_token, return_tensors='pt').to(device)  # 사용자 입력 데이터 변환
        # 답변 생성
        output_ids = model.generate(input_ids, min_length=10, max_length=512, eos_token_id=tokenizer.eos_token_id, early_stopping=True, no_repeat_ngram_size=2, length_penalty=0.7, temperature=0.7, top_k=50, top_p=0.95)

        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        # 생성된 응답에서 질문 부분 제거
        if response.startswith(question):
        # 질문 문자열 길이만큼 응답 문자열에서 제거
            response = response[len(question):].strip()
        return response

# 모델 불러오기
model = KoGPT2ChatModel(model)  # 모델 인스턴스 생성

PATH = 'KoGPT2_Mul.pt'  # 경로

device = torch.device('cpu')    # cpu 설정
model.load_state_dict(torch.load(PATH, map_location=device))    # 모델 설정 및 가중치 불러오기