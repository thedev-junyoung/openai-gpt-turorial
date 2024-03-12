import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from cost_calculator import calculate_costs

class OpenAIAssistant:
    def __init__(self, api_key: str, model: str, assistant_name: str, instructions: str, tools: list):
        """
        Initialize the OpenAI Assistant class.
        OpenAI Assistant 클래스를 초기화

        Args:
            api_key (str): API key for accessing the OpenAI API. (OpenAI API에 접근하기 위한 API 키)
            model (str): Model to use for the assistant. (어시스턴트에 사용할 모델)
            assistant_name (str): Name of the assistant. (어시스턴트의 이름)
            instructions (str): Instructions for the assistant. (어시스턴트의 작업 지시사항)
            tools (list): List of tools required for the assistant. (어시스턴트에 필요한 도구의 목록)
        """
        self.client: OpenAI = OpenAI(api_key=api_key)  # Initialize OpenAI client object (OpenAI 클라이언트 객체를 초기화)
        self.model = model  # Set the model information (모델 정보를 설정)
        self.assistant_name = assistant_name  # Set the name of the assistant (어시스턴트의 이름을 설정)
        self.instructions = instructions  # Set the instructions for the assistant (어시스턴트의 지시사항을 설정)
        self.tools = tools  # Set the list of tools used by the assistant (어시스턴트에 사용되는 도구 목록을 설정)
        self.assistant = self.create_assistant()  # Initialize the assistant by calling the create_assistant method (create_assistant 메서드를 호출하여 어시스턴트를 초기화)
        self.thread = self.create_thread()  # Initialize the thread by calling the create_thread method (create_thread 메서드를 호출하여 스레드를 초기화)

    def create_assistant(self):
        """
        Create the assistant.
        어시스턴트를 생성
        """
        return self.client.beta.assistants.create(
            name=self.assistant_name,
            instructions=self.instructions,
            tools=self.tools,
            model=self.model
        )

    def create_thread(self):
        """
        Create a new thread.
        새로운 스레드를 생성
        """
        return self.client.beta.threads.create()

    def add_system_message(self, content: str):
        """
        Add a system message to the thread.
        시스템 메시지를 스레드에 추가
        """
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            content=content,
            role="user"  # 'system' role not supported by API
        )

    def send_user_message(self, content: str):
        """
        Send a user message to the thread.
        사용자 메시지를 스레드에 전송
        """
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            content=content,
            role="user",
        )

    def run_assistant(self, instructions: str):
        """
        Run the assistant.
        어시스턴트를 실행
        """
        return self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )

    def get_run_response(self, run):
        """
        Get the run response.
        실행 결과를 가져옵니다.
        """
        time.sleep(5)  # Wait for the execution to complete (실행이 완료되기까지 대기)
        return self.client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=run.id
        )

    def display_response(self):
        """
        Display the assistant's response.
        어시스턴트의 응답을 표시
        """
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        for message in messages.data:
            if message.role == "assistant":
                print(f"Assistant: {message.content}")

    def start(self, user_instructions: str):
        """
        Start the assistant.
        어시스턴트를 시작
        """

        while True:
            user_input = input("You: ")  # Get user input (사용자 입력을 받음.)
            if user_input.lower() in ["exit", "quit"]:
                break
            self.send_user_message(user_input)  # Send the user message (사용자 메시지를 전송)
            run = self.run_assistant(user_instructions)  # Run the assistant (어시스턴트를 실행)
            response = self.get_run_response(run)  # Get the run response (실행 결과를 가져옴)
            calculate_costs(response)  
            self.display_response()  # Display the assistant's response (어시스턴트의 응답을 표시)



if __name__ == "__main__":
    # Load environment variables from the .env file
    # .env 파일에서 환경 변수 로드
    load_dotenv()
    
    # Get API key from the .env file
    # .env 파일에서 API 키 가져오기
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Instantiate the OpenAIAssistant class
    # OpenAIAssistant 클래스의 인스턴스 생성
    assistant = OpenAIAssistant(
        api_key=OPENAI_API_KEY,
        model="gpt-4-turbo-preview",
        assistant_name="General Assistant",
        instructions="You are a versatile assistant. Answer questions to the best of your knowledge and run code if necessary.",
        tools=[{"type": "code_interpreter"}]
    )
    # run
    assistant_instructions = "Please address the user appropriately. They have a premium account."
    assistant.start(user_instructions=assistant_instructions)