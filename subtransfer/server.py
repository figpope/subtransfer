from flask import Flask, request
import praw

import settings

app = Flask(__name__)

CLIENT = None


def _get_praw_client():
    global CLIENT
    if not CLIENT:
        CLIENT = praw.Reddit(settings.USER_AGENT)
        CLIENT.set_oauth_app_info(
            settings.CLIENT_ID,
            settings.CLIENT_SECRET,
            settings.HOST + settings.REDIRECT_URI
        )
    return CLIENT

@app.route('/')
def homepage():
    r = _get_praw_client()
    auth_link = "<a href=%s>here</a>" % r.get_authorize_url('first_account', 'mysubreddits')
    text = "Please log into the account you want to transfer your subreddit subscriptions from, then click %s." % auth_link
    return text

SUBREDDITS_FOUND = []

@app.route(settings.REDIRECT_URI)
def authorized():
    global SUBREDDITS_FOUND

    state = request.args.get('state', '')
    code = request.args.get('code', '')

    r = _get_praw_client()
    info = r.get_access_information(code, update_session=True)
    if state == 'first_account':
        SUBREDDITS_FOUND = list(r.get_my_subreddits(limit=None))
        auth_link = "<a href=%s>here</a>" % r.get_authorize_url('second_account', 'subscribe')
        return ('Now, please logout of your Reddit account, and'
                ' log into the account you want to transfer the subreddits to. '
                'Once you\'ve logged in, please click %s.' % auth_link)
    elif state == 'second_account':
        for subreddit in SUBREDDITS_FOUND:
            r.subscribe(subreddit)
            print subreddit
        return ('Subreddits transferred!')

    variables_text = "State=%s, code=%s, info=%s." % (state, code,
                                                      str(info))
    back_link = "<a href='/'>Try again</a>"
    return variables_text + '</br></br>' + back_link

if __name__ == '__main__':
    app.run(debug=True, port=65010)