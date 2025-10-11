from longcodezip import CodeCompressor
from loguru import logger

if __name__ == "__main__":

    with open("assets/example_context.py", "r") as f:
        context = f.read()

    question = '''
    async def _finalize_step(
        self, step: "AgentStep", messages: list["LLMMessage"], execution: "AgentExecution"
    ) -> None:
        step.state = AgentStepState.COMPLETED
    '''
   
    # Initialize compressor
    logger.info("Initializing compressor...")
    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"
    compressor = CodeCompressor(model_name=model_name)
    
    # Test function-based code file compression with query
    logger.info("\nTesting function-based code file compression with query...")

    original_tokens = len(compressor.tokenizer.encode(context))
    target_token = 64
    target_ratio = min(1.0, max(0.0, target_token / original_tokens))
    logger.info(f"CodeCompressor: Original tokens={original_tokens}, Target tokens={target_token}, Calculated ratio={target_ratio:.4f}")

    logger.info("\nTesting compression with Coarse-grained compression only...")
    result_cond = compressor.compress_code_file(
        code=context,
        query=question,
        instruction="Complete the following code function given the context.",
        rate=target_ratio,
        rank_only=True # Coarse-grained compression
    )
    logger.info(f"Compressed prompt: \n{result_cond['compressed_prompt']}")

    logger.info("\nTesting compression with Coarse-grained and Fine-grained compression...")
    result_cond = compressor.compress_code_file(
        code=context,
        query=question,
        instruction="Complete the following code function given the context.",
        rate=target_ratio,
        rank_only=False # Corase-grained and Fine-grained compression
    )
    logger.info(f"Compressed prompt: \n{result_cond['compressed_prompt']}")