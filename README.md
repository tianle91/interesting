# interesting
Uses loss of a `gpt2` language model to evaluate interestingness of a reddit submission.
![screenshot](screenshot.png)

Running `docker-compose up` should work.
Then navigate to [localhost:5001](localhost:5001).

## requirements
You'll need a [`praw.ini`](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html) file.

You need to provide a `HF_INFERENCE_URL`, where an instance of [`tianle91/hf-inference`](https://github.com/tianle91/hf-inference) is deployed.
