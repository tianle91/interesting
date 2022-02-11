from typing import Callable

from transformers import GPT2LMHeadModel, GPT2Tokenizer


def get_interest_rater(rater_name: str = 'gpt2') -> Callable[[str], float]:
    if rater_name == 'gpt2':
        gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        gpt2_lmhead = GPT2LMHeadModel.from_pretrained('gpt2')

        def f(s):
            inputs = gpt2_tokenizer(s, return_tensors="pt")
            outputs = gpt2_lmhead(**inputs, labels=inputs["input_ids"])
            return float(outputs.loss)
        return f
