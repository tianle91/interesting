from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")


def get_interest(s):
    inputs = tokenizer(s, return_tensors="pt")
    outputs = model(**inputs, labels=inputs["input_ids"])
    return outputs.loss
