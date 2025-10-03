from longcodezip import CodeCompressor
from loguru import logger

if __name__ == "__main__":

    context = """
    def add(a, b):
        return a + b

    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

    def search_with_binary_search(arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    """

    question = "How to write a quick sort algorithm?"
   
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

    result = compressor.compress_code_file(
        code=context,
        query=question, # Using current function context as query focus
        instruction="Complete the following code function given the context.",
        rate=target_ratio,
        rank_only=False, # False to use fine-grained compression
        fine_grained_importance_method="contrastive_perplexity", # Explicitly test default
        min_lines_for_fine_grained=5, # Min number of lines for fine-grained compression
        importance_beta=0.5, # Sensitivity to importance score
        use_knapsack=True,
    )

    # show the compressed code
    logger.info(f"Compressed code (using {result['fine_grained_method_used']}): \n{result['compressed_code']}")
    logger.info(f"Current function context: \n{question}")
    # final prompt
    final_prompt = result['compressed_prompt']
    # get the completion
    tokenized_prompt = compressor.tokenizer(final_prompt, return_tensors="pt").to(compressor.device)
    # Increase max_new_tokens for potentially longer completions
    completion_ids = compressor.model.generate(**tokenized_prompt, max_new_tokens=128, pad_token_id=compressor.tokenizer.eos_token_id)
    # Decode only the generated part, skipping special tokens
    completion = compressor.tokenizer.decode(completion_ids[0][len(tokenized_prompt.input_ids[0]):], skip_special_tokens=True)

    # Basic cleanup: remove leading/trailing whitespace and potentially stop words if needed
    completion = completion.strip()
    # More robust cleanup: Find the first meaningful line if generation includes noise
    completion_lines = [line for line in completion.split("\n") if line.strip() and not line.strip().startswith(("#", "//"))] # Simple comment removal
    cleaned_completion = completion_lines[0] if completion_lines else completion # Take first non-comment line or original if none found

    logger.info(f"Cleaned Completion: {cleaned_completion}")

    # Optional: Test with conditional_ppl method
    logger.info("\nTesting fine-grained compression with conditional_ppl...")
    result_cond = compressor.compress_code_file(
        code=context,
        query=question,
        instruction="Complete the following code function given the context.",
        rate=target_ratio,
        rank_only=False,
        fine_grained_importance_method="conditional_ppl",
        min_lines_for_fine_grained=5,
        importance_beta=0.5
    )
    logger.info(f"Compressed code (using {result_cond['fine_grained_method_used']}): \n{result_cond['compressed_code']}")