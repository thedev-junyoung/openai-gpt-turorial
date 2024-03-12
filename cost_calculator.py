from enum import Enum
from openai.types.chat import ChatCompletion

class ModelCost(Enum):
    GPT_4_TURBO_PREVIEW = ("gpt-4-turbo-preview", 0.01, 0.03)
    GPT_3_5_TURBO = ("gpt-3.5-turbo", 0.005, 0.015)

class ToolCost(Enum):
    CODE_INTERPRETER = 0.03  # per session
    RETRIEVAL = 0.20  # per GB per day

# 이 함수는 특정 모델에 대한 입력 및 출력 비용을 계산합니다.
def calculate_costs(response: ChatCompletion, model_name: str) -> None:
    """
    Calculate the costs of input and output for a specific model.
    특정 모델에 대한 입력 및 출력 비용을 계산합니다.

    Args:
        response (ChatCompletion): Response from the OpenAI API. (OpenAI API의 응답입니다.)
        model_name (str): Name of the model. (모델의 이름입니다.)

    Returns:
        None
    """
    model = next((m for m in ModelCost if m.value[0] == model_name), None)
    if model is None:
        raise ValueError(f"모델 이름 {model_name}은 유효하지 않습니다.")
    
    completion_tokens = response.usage.completion_tokens
    prompt_tokens = response.usage.prompt_tokens
    input_cost_rate = model.value[1]
    output_cost_rate = model.value[2]
    input_cost = (prompt_tokens / 1000) * input_cost_rate
    output_cost = (completion_tokens / 1000) * output_cost_rate
    # 총 비용 계산
    total_cost = input_cost + output_cost

    print(f"Input cost for {model.name}: ${input_cost}")
    print(f"Output cost for {model.name}: ${output_cost}")
    print(f"Total cost: ${total_cost}")