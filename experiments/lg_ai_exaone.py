from pathlib import Path

from llama_cpp import Llama

exaone = rf'{Path(__file__).parents[1]}\models\EXAONE-3.5-2.4B-Instruct-GGUF\EXAONE-3.5-2.4B-Instruct-Q4_K_M.gguf'

llm = Llama(exaone)

completion = llm.create_chat_completion(
                                            messages = [
                                                {
                                                    "role": "user",
                                                    "content": "What is the capital of France?"
                                                }
                                            ]
                                        )

print(completion['choices'][0]['message']['content'])