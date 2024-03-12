import os
from dotenv import load_dotenv
from typing import Dict, Any
from openai import OpenAI
from openai.types.chat import ChatCompletion
from cost_calculator import calculate_costs

class OpenAICompletion:
    """
    Initialize the OpenAICompletion class.
    OpenAICompletion 클래스를 초기화합니다.

    Args:
        model_name (str): Name of the OpenAI model to use. (사용할 OpenAI 모델의 이름)
        open_ai_key (str): API key for accessing the OpenAI API. (OpenAI API에 접근하기 위한 API 키)
    """
    def __init__(self, model_name: str, open_ai_key:str):
        self.client: OpenAI = OpenAI(api_key=open_ai_key)
        self.model_name = model_name
    
    def call_openai_api(self, model: str, messages: list) -> Dict[str, Any]:
        """
        Call the OpenAI API.
        OpenAI API를 호출합니다.

        Args:
            model (str): Name of the OpenAI model to use. (사용할 OpenAI 모델의 이름)
            messages (list): List of message dictionaries. (메시지 사전들의 목록)

        Returns:
            Dict[str, Any]: Response from the OpenAI API. (OpenAI API 응답)
        """
        try:
            # API 호출
            response = self.client.chat.completions.create(
                model=model,
                response_format={ "type": "json_object" },
                messages=messages,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                max_tokens=4095
            )
            return response
        except Exception as e:
            # API 호출 중 오류 발생 시 처리
            print(f"API 호출 중 오류 발생: {e}")
            return {}

    def generate(self, system_input: str, content_input: str) -> Dict[str, Any]:
        """
        Generate response using OpenAI API.
        OpenAI API를 사용하여 응답을 생성합니다.

        Args:
            system_input (str): System input message. (시스템 입력 메시지)
            content_input (str): Content input message. (컨텐츠 입력 메시지)

        Returns:
            Dict[str, Any]: Response generated by the OpenAI model. (OpenAI 모델에 의해 생성된 응답)
        """
        messages = [
            {"role": "system", "content": system_input},
            {"role": "user", "content": content_input},
        ]
        response:ChatCompletion = self.call_openai_api(self.model_name, messages)
        calculate_costs(response,self.model_name)
        return response.choices[0].message.content  # JSON 모드 사용으로 인해 별도의 파싱 불필요

# 사용
if __name__ == "__main__":
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    service = OpenAICompletion(model_name="gpt-3.5-turbo",open_ai_key=OPENAI_API_KEY)  # 사용할 모델을 초기화할 때 지정
    system_prompt = "You are a helpful assistant designed to output JSON."
    user_input = "Who won the world series in 2020?"
    result = service.generate(system_prompt, user_input)
    print(result)