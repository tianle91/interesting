from flask import Flask, redirect, render_template, request, url_for

from interesting import get_interests, reddit

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for(endpoint='show_interesting_submissions', subreddit='all'))


@app.route('/r/<subreddit>', methods=['GET', 'POST'])
def show_interesting_submissions(subreddit: str):
    if request.method == 'POST':
        subreddit = request.form['subreddit']
        return redirect(url_for(endpoint='show_interesting_submissions', subreddit=subreddit))

    submissions = list(
        reddit
        .subreddit(display_name=subreddit)
        .top(time_filter='day', limit=25)
    )
    interests = get_interests(submissions)
    submissions.sort(key=lambda x: interests[x.id], reverse=True)

    content = []
    for submission in submissions:
        comments_url = f'https://www.reddit.com{submission.permalink}'
        # content is url if exists else comment
        content_url = submission.url if len(submission.selftext) > 0 else comments_url
        # if submission url is image then embed it
        image_url = submission.url if submission.url.endswith(('.jpg', '.png')) else None
        # if self text is too long then truncate
        selftext = submission.selftext
        if len(selftext) > 200:
            selftext = selftext[:200] + '...'

        content.append({
            'title': submission.title,
            'content_url': content_url,
            'subreddit': submission.subreddit.display_name,
            'comments_url': comments_url,
            'image_url': image_url,
            'selftext': selftext,
            'num_comments': submission.num_comments,
            'interest': f'{interests[submission.id]:.2f}',
            'score': submission.score,
            'upvote_ratio': submission.upvote_ratio
        })
    return render_template('subreddit.html', res={'subreddit': subreddit, 'content': content})
