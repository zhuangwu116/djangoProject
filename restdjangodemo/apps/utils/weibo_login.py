def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_url = "http://47.92.87.172:8000/complete/weibo/"
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={re_url}".format(client_id="", re_url=redirect_url)
    print(auth_url)
