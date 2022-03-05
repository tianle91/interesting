# interesting
Uses loss of a `gpt2` language model to evaluate interestingness of a reddit submission.
![screenshot](screenshot.png)

Running `docker-compose up` should work.
Then navigate to [localhost:5001](http://localhost:5001).
You can also see it live [here](https://interesting-343114.ue.r.appspot.com).


## requirements
You'll need a [`praw.ini`](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html) file.

You need to provide a `HF_INFERENCE_URL` in [Dockerfile](./Dockerfile), where an instance of [`tianle91/hf-inference`](https://github.com/tianle91/hf-inference) is deployed.
Currently it's just my own desktop server, which may or may not be on.
