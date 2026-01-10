from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate

MODEL_PATH = r"D:\Mentor\LLM_MODELS\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

llm = LlamaCpp(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=0,
    temperature=0.3
)

prompt = PromptTemplate.from_template(
    "You are a helpful AI teacher.\n\nQuestion: {question}\n\nAnswer step by step:"
)

chain = prompt | llm

response = chain.invoke({"question": "What is AI?"})
print(response)
