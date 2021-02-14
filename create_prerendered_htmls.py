import re
import sqlalchemy
import yaml
import pandas as pd
import os
import random


config = yaml.safe_load(open('config.yml'))
no_poster = 'https://flibo-images.s3-us-west-2.amazonaws.com/posters/no-poster.png'
no_cover = 'https://flibo-images.s3-us-west-2.amazonaws.com/covers/no-cover.jpg'

if not os.path.exists(config['prerendered_htmls_directory']):
    os.makedirs(config['prerendered_htmls_directory'])

try:
    df_contents_info = pd.read_csv('contents_info.csv')
except:
    print('Fetching contents...')
    engine = sqlalchemy.create_engine(
        'postgres://' + config['sql']['user'] + ':' + config['sql']['password'] + '@' + config['sql'][
            'host'] + ':' + str(config['sql']['port']) + '/' + config['sql']['db'])
    con = engine.connect()
    script = """select content_id, title, imdb_score, poster, cover, similar_content, genres, type, summary_text,
                       where_to_watch_united_states as where_to_watch, main_artists, url_title, youtube_trailer_id
                from app.content_details
                order by num_votes desc"""
    df_contents_info = pd.read_sql(script, con=con)
    df_contents_info.to_csv('contents_info.csv', index=False)
    df_contents_info = pd.read_csv('contents_info.csv')
    con.close()

print('Cleaning content info...')
df_contents_info = df_contents_info.where((pd.notnull(df_contents_info)), None)
df_contents_info['similar_content'] = df_contents_info['similar_content'].apply(lambda x: eval(x) if x else [])
df_contents_info['where_to_watch'] = df_contents_info['where_to_watch'].apply(lambda x: eval(x) if x else None)
df_contents_info['where_to_watch'] = df_contents_info['where_to_watch'].apply(lambda x: x.get('stream', x.get('rent', x.get('buy'))) if x else None)
df_contents_info['genres'] = df_contents_info['genres'].apply(lambda genres: [x.replace("'", '') for x in eval(genres)] if genres else genres)
df_contents_info['main_artists'] = df_contents_info['main_artists'].apply(lambda artists: [x.replace("'", '') for x in eval(artists)] if artists else [])

print('Dropping duplicate slugs...')
df_main_contents = df_contents_info.drop_duplicates('url_title')

print(f'Datframe size - {df_main_contents.shape[0]}')
i = 0
for content in df_main_contents.to_dict(orient='records'):
    i += 1
    if content['similar_content']:
        content_type = 'movie' if content['type'] == 'movie' else 'show'
        if i % 100 == 0:
            print(i, f"{content_type}s-like-{content['url_title']}")

        page_html = """
        <!DOCTYPE html><html lang="en"><head><link rel="icon" href="/favicon.png"><link rel="prefetch" href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900"><link rel="prefetch" href="https://cdn.jsdelivr.net/npm/@mdi/font@latest/css/materialdesignicons.min.css"><link href="/css/Article.<css_article_hash>.css" rel="prefetch"><link href="/css/ArticleOnDemand.<css_article_on_demand_hash>.css" rel="prefetch"><link href="/css/Home.<css_home_hash>.css" rel="prefetch"><link href="/js/Article.<js_article_hash>.js" rel="prefetch"><link href="/js/ArticleOnDemand.<js_article_on_demand_hash>.js" rel="prefetch"><link href="/js/Home.<js_home_hash>.js" rel="prefetch"><link href="/css/app.<css_app_hash>.css" rel="preload" as="style"><link href="/css/chunk-vendors.<css_chunk_vendors_hash>.css" rel="preload" as="style"><link href="/js/app.<js_app_hash>.js" rel="preload" as="script"><link href="/js/chunk-vendors.<js_chunk_vendors_hash>.js" rel="preload" as="script"><link href="/css/chunk-vendors.<css_chunk_vendors_hash>.css" rel="stylesheet"><link href="/css/app.<css_app_hash>.css" rel="stylesheet"><link href="https://www.googletagmanager.com" rel="preconnect"> <script type="text/javascript" async="" src="https://www.google-analytics.com/analytics.js"></script><script async="" src="https://www.googletagmanager.com/gtag/js?id=UA-163755956-1" charset="utf-8"></script><link rel="stylesheet" type="text/css" href="/css/Article.<css_article_hash>.css"> <script charset="utf-8" src="/js/Article.<js_article_hash>.js"></script><style data-vue-meta="vuetify" type="text/css" id="vuetify-theme-stylesheet" nonce="undefined">.v-application a{color:#1976d2}.v-application .primary{background-color:#1976d2 !important;border-color:#1976d2 !important}.v-application .primary--text{color:#1976d2 !important;caret-color:#1976d2 !important}.v-application .primary.lighten-5{background-color:#c7fdff !important;border-color:#c7fdff !important}.v-application .primary--text.text--lighten-5{color:#c7fdff !important;caret-color:#c7fdff !important}.v-application .primary.lighten-4{background-color:#a8e0ff !important;border-color:#a8e0ff !important}.v-application .primary--text.text--lighten-4{color:#a8e0ff !important;caret-color:#a8e0ff !important}.v-application .primary.lighten-3{background-color:#8ac5ff !important;border-color:#8ac5ff !important}.v-application .primary--text.text--lighten-3{color:#8ac5ff !important;caret-color:#8ac5ff !important}.v-application .primary.lighten-2{background-color:#6aaaff !important;border-color:#6aaaff !important}.v-application .primary--text.text--lighten-2{color:#6aaaff !important;caret-color:#6aaaff !important}.v-application .primary.lighten-1{background-color:#488fef !important;border-color:#488fef !important}.v-application .primary--text.text--lighten-1{color:#488fef !important;caret-color:#488fef !important}.v-application .primary.darken-1{background-color:#005eb6 !important;border-color:#005eb6 !important}.v-application .primary--text.text--darken-1{color:#005eb6 !important;caret-color:#005eb6 !important}.v-application .primary.darken-2{background-color:#00479b !important;border-color:#00479b !important}.v-application .primary--text.text--darken-2{color:#00479b !important;caret-color:#00479b !important}.v-application .primary.darken-3{background-color:#003180 !important;border-color:#003180 !important}.v-application .primary--text.text--darken-3{color:#003180 !important;caret-color:#003180 !important}.v-application .primary.darken-4{background-color:#001e67 !important;border-color:#001e67 !important}.v-application .primary--text.text--darken-4{color:#001e67 !important;caret-color:#001e67 !important}.v-application .secondary{background-color:#424242 !important;border-color:#424242 !important}.v-application .secondary--text{color:#424242 !important;caret-color:#424242 !important}.v-application .secondary.lighten-5{background-color:#c1c1c1 !important;border-color:#c1c1c1 !important}.v-application .secondary--text.text--lighten-5{color:#c1c1c1 !important;caret-color:#c1c1c1 !important}.v-application .secondary.lighten-4{background-color:#a6a6a6 !important;border-color:#a6a6a6 !important}.v-application .secondary--text.text--lighten-4{color:#a6a6a6 !important;caret-color:#a6a6a6 !important}.v-application .secondary.lighten-3{background-color:#8b8b8b !important;border-color:#8b8b8b !important}.v-application .secondary--text.text--lighten-3{color:#8b8b8b !important;caret-color:#8b8b8b !important}.v-application .secondary.lighten-2{background-color:#727272 !important;border-color:#727272 !important}.v-application .secondary--text.text--lighten-2{color:#727272 !important;caret-color:#727272 !important}.v-application .secondary.lighten-1{background-color:#595959 !important;border-color:#595959 !important}.v-application .secondary--text.text--lighten-1{color:#595959 !important;caret-color:#595959 !important}.v-application .secondary.darken-1{background-color:#2c2c2c !important;border-color:#2c2c2c !important}.v-application .secondary--text.text--darken-1{color:#2c2c2c !important;caret-color:#2c2c2c !important}.v-application .secondary.darken-2{background-color:#171717 !important;border-color:#171717 !important}.v-application .secondary--text.text--darken-2{color:#171717 !important;caret-color:#171717 !important}.v-application .secondary.darken-3{background-color:#000 !important;border-color:#000 !important}.v-application .secondary--text.text--darken-3{color:#000 !important;caret-color:#000 !important}.v-application .secondary.darken-4{background-color:#000 !important;border-color:#000 !important}.v-application .secondary--text.text--darken-4{color:#000 !important;caret-color:#000 !important}.v-application .accent{background-color:#82b1ff !important;border-color:#82b1ff !important}.v-application .accent--text{color:#82b1ff !important;caret-color:#82b1ff !important}.v-application .accent.lighten-5{background-color:#fff !important;border-color:#fff !important}.v-application .accent--text.text--lighten-5{color:#fff !important;caret-color:#fff !important}.v-application .accent.lighten-4{background-color:#f8ffff !important;border-color:#f8ffff !important}.v-application .accent--text.text--lighten-4{color:#f8ffff !important;caret-color:#f8ffff !important}.v-application .accent.lighten-3{background-color:#daffff !important;border-color:#daffff !important}.v-application .accent--text.text--lighten-3{color:#daffff !important;caret-color:#daffff !important}.v-application .accent.lighten-2{background-color:#bce8ff !important;border-color:#bce8ff !important}.v-application .accent--text.text--lighten-2{color:#bce8ff !important;caret-color:#bce8ff !important}.v-application .accent.lighten-1{background-color:#9fccff !important;border-color:#9fccff !important}.v-application .accent--text.text--lighten-1{color:#9fccff !important;caret-color:#9fccff !important}.v-application .accent.darken-1{background-color:#6596e2 !important;border-color:#6596e2 !important}.v-application .accent--text.text--darken-1{color:#6596e2 !important;caret-color:#6596e2 !important}.v-application .accent.darken-2{background-color:#467dc6 !important;border-color:#467dc6 !important}.v-application .accent--text.text--darken-2{color:#467dc6 !important;caret-color:#467dc6 !important}.v-application .accent.darken-3{background-color:#2364aa !important;border-color:#2364aa !important}.v-application .accent--text.text--darken-3{color:#2364aa !important;caret-color:#2364aa !important}.v-application .accent.darken-4{background-color:#004c90 !important;border-color:#004c90 !important}.v-application .accent--text.text--darken-4{color:#004c90 !important;caret-color:#004c90 !important}.v-application .error{background-color:#ff5252 !important;border-color:#ff5252 !important}.v-application .error--text{color:#ff5252 !important;caret-color:#ff5252 !important}.v-application .error.lighten-5{background-color:#ffe4d5 !important;border-color:#ffe4d5 !important}.v-application .error--text.text--lighten-5{color:#ffe4d5 !important;caret-color:#ffe4d5 !important}.v-application .error.lighten-4{background-color:#ffc6b9 !important;border-color:#ffc6b9 !important}.v-application .error--text.text--lighten-4{color:#ffc6b9 !important;caret-color:#ffc6b9 !important}.v-application .error.lighten-3{background-color:#ffa99e !important;border-color:#ffa99e !important}.v-application .error--text.text--lighten-3{color:#ffa99e !important;caret-color:#ffa99e !important}.v-application .error.lighten-2{background-color:#ff8c84 !important;border-color:#ff8c84 !important}.v-application .error--text.text--lighten-2{color:#ff8c84 !important;caret-color:#ff8c84 !important}.v-application .error.lighten-1{background-color:#ff6f6a !important;border-color:#ff6f6a !important}.v-application .error--text.text--lighten-1{color:#ff6f6a !important;caret-color:#ff6f6a !important}.v-application .error.darken-1{background-color:#df323b !important;border-color:#df323b !important}.v-application .error--text.text--darken-1{color:#df323b !important;caret-color:#df323b !important}.v-application .error.darken-2{background-color:#bf0025 !important;border-color:#bf0025 !important}.v-application .error--text.text--darken-2{color:#bf0025 !important;caret-color:#bf0025 !important}.v-application .error.darken-3{background-color:#9f0010 !important;border-color:#9f0010 !important}.v-application .error--text.text--darken-3{color:#9f0010 !important;caret-color:#9f0010 !important}.v-application .error.darken-4{background-color:#800000 !important;border-color:#800000 !important}.v-application .error--text.text--darken-4{color:#800000 !important;caret-color:#800000 !important}.v-application .info{background-color:#2196f3 !important;border-color:#2196f3 !important}.v-application .info--text{color:#2196f3 !important;caret-color:#2196f3 !important}.v-application .info.lighten-5{background-color:#d4ffff !important;border-color:#d4ffff !important}.v-application .info--text.text--lighten-5{color:#d4ffff !important;caret-color:#d4ffff !important}.v-application .info.lighten-4{background-color:#b5ffff !important;border-color:#b5ffff !important}.v-application .info--text.text--lighten-4{color:#b5ffff !important;caret-color:#b5ffff !important}.v-application .info.lighten-3{background-color:#95e8ff !important;border-color:#95e8ff !important}.v-application .info--text.text--lighten-3{color:#95e8ff !important;caret-color:#95e8ff !important}.v-application .info.lighten-2{background-color:#75ccff !important;border-color:#75ccff !important}.v-application .info--text.text--lighten-2{color:#75ccff !important;caret-color:#75ccff !important}.v-application .info.lighten-1{background-color:#51b0ff !important;border-color:#51b0ff !important}.v-application .info--text.text--lighten-1{color:#51b0ff !important;caret-color:#51b0ff !important}.v-application .info.darken-1{background-color:#007cd6 !important;border-color:#007cd6 !important}.v-application .info--text.text--darken-1{color:#007cd6 !important;caret-color:#007cd6 !important}.v-application .info.darken-2{background-color:#0064ba !important;border-color:#0064ba !important}.v-application .info--text.text--darken-2{color:#0064ba !important;caret-color:#0064ba !important}.v-application .info.darken-3{background-color:#004d9f !important;border-color:#004d9f !important}.v-application .info--text.text--darken-3{color:#004d9f !important;caret-color:#004d9f !important}.v-application .info.darken-4{background-color:#003784 !important;border-color:#003784 !important}.v-application .info--text.text--darken-4{color:#003784 !important;caret-color:#003784 !important}.v-application .success{background-color:#4caf50 !important;border-color:#4caf50 !important}.v-application .success--text{color:#4caf50 !important;caret-color:#4caf50 !important}.v-application .success.lighten-5{background-color:#dcffd6 !important;border-color:#dcffd6 !important}.v-application .success--text.text--lighten-5{color:#dcffd6 !important;caret-color:#dcffd6 !important}.v-application .success.lighten-4{background-color:#beffba !important;border-color:#beffba !important}.v-application .success--text.text--lighten-4{color:#beffba !important;caret-color:#beffba !important}.v-application .success.lighten-3{background-color:#a2ff9e !important;border-color:#a2ff9e !important}.v-application .success--text.text--lighten-3{color:#a2ff9e !important;caret-color:#a2ff9e !important}.v-application .success.lighten-2{background-color:#85e783 !important;border-color:#85e783 !important}.v-application .success--text.text--lighten-2{color:#85e783 !important;caret-color:#85e783 !important}.v-application .success.lighten-1{background-color:#69cb69 !important;border-color:#69cb69 !important}.v-application .success--text.text--lighten-1{color:#69cb69 !important;caret-color:#69cb69 !important}.v-application .success.darken-1{background-color:#2d9437 !important;border-color:#2d9437 !important}.v-application .success--text.text--darken-1{color:#2d9437 !important;caret-color:#2d9437 !important}.v-application .success.darken-2{background-color:#00791e !important;border-color:#00791e !important}.v-application .success--text.text--darken-2{color:#00791e !important;caret-color:#00791e !important}.v-application .success.darken-3{background-color:#006000 !important;border-color:#006000 !important}.v-application .success--text.text--darken-3{color:#006000 !important;caret-color:#006000 !important}.v-application .success.darken-4{background-color:#004700 !important;border-color:#004700 !important}.v-application .success--text.text--darken-4{color:#004700 !important;caret-color:#004700 !important}.v-application .warning{background-color:#fb8c00 !important;border-color:#fb8c00 !important}.v-application .warning--text{color:#fb8c00 !important;caret-color:#fb8c00 !important}.v-application .warning.lighten-5{background-color:#ffff9e !important;border-color:#ffff9e !important}.v-application .warning--text.text--lighten-5{color:#ffff9e !important;caret-color:#ffff9e !important}.v-application .warning.lighten-4{background-color:#fffb82 !important;border-color:#fffb82 !important}.v-application .warning--text.text--lighten-4{color:#fffb82 !important;caret-color:#fffb82 !important}.v-application .warning.lighten-3{background-color:#ffdf67 !important;border-color:#ffdf67 !important}.v-application .warning--text.text--lighten-3{color:#ffdf67 !important;caret-color:#ffdf67 !important}.v-application .warning.lighten-2{background-color:#ffc24b !important;border-color:#ffc24b !important}.v-application .warning--text.text--lighten-2{color:#ffc24b !important;caret-color:#ffc24b !important}.v-application .warning.lighten-1{background-color:#ffa72d !important;border-color:#ffa72d !important}.v-application .warning--text.text--lighten-1{color:#ffa72d !important;caret-color:#ffa72d !important}.v-application .warning.darken-1{background-color:#db7200 !important;border-color:#db7200 !important}.v-application .warning--text.text--darken-1{color:#db7200 !important;caret-color:#db7200 !important}.v-application .warning.darken-2{background-color:#bb5900 !important;border-color:#bb5900 !important}.v-application .warning--text.text--darken-2{color:#bb5900 !important;caret-color:#bb5900 !important}.v-application .warning.darken-3{background-color:#9d4000 !important;border-color:#9d4000 !important}.v-application .warning--text.text--darken-3{color:#9d4000 !important;caret-color:#9d4000 !important}.v-application .warning.darken-4{background-color:#802700 !important;border-color:#802700 !important}.v-application .warning--text.text--darken-4{color:#802700 !important;caret-color:#802700 !important}</style><title>Top 10 awesome {contents} like {content_title} that you will enjoy watching</title><meta data-vue-meta="1" http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta data-vue-meta="1" data-vmid="viewport" name="viewport" content="width=device-width, initial-scale=1"><meta data-vue-meta="1" data-vmid="og:type" property="og:type" content="website"><meta data-vue-meta="1" data-vmid="twitter:card" name="twitter:card" content="summary"><link rel="stylesheet" type="text/css" href="/css/ArticleOnDemand.<css_article_on_demand_hash>.css"> <script charset="utf-8" src="/js/ArticleOnDemand.<js_article_on_demand_hash>.js"></script><meta data-vue-meta="1" data-vmid="og:url" property="og:url" content="https://blog.flibo.ai/{contents}-like-{page_slug}"><meta data-vue-meta="1" data-vmid="twitter:url" name="twitter:url" content="https://blog.flibo.ai/{contents}-like-{page_slug}"><meta data-vue-meta="1" data-vmid="description" name="description" content="Are you looking for {contents} like {content_title}? We have curated a list for you, a list of {contents} by the likes of {page_artists}."><meta data-vue-meta="1" data-vmid="og:title" property="og:title" content="Top 10 awesome {contents} like {content_title} that you will enjoy watching"><meta data-vue-meta="1" data-vmid="og:description" property="og:description" content="Are you looking for {contents} like {content_title}? We have curated a list for you, a list of {contents} by the likes of {page_artists}."><meta data-vue-meta="1" data-vmid="og:image" property="og:image" content="{page_cover}"><meta data-vue-meta="1" data-vmid="twitter:title" name="twitter:title" content="Top 10 awesome {contents} like {content_title} that you will enjoy watching"><meta data-vue-meta="1" data-vmid="twitter:description" name="twitter:description" content="Are you looking for {contents} like {content_title}? We have curated a list for you, a list of {contents} by the likes of {page_artists}."><meta data-vue-meta="1" data-vmid="twitter:image" name="twitter:image" content="{page_cover}"></head><body> <noscript><strong>We're sorry but flibo-blog-temp doesn't work properly without JavaScript enabled. Please enable it to continue.</strong></noscript><div data-app="true" class="v-application v-application--is-ltr theme--light" id="app"><div class="v-application--wrap"> <header class="top-bar v-sheet v-sheet--tile theme--light v-toolbar v-toolbar--flat v-app-bar v-app-bar--fixed white" style="height: 90px; margin-top: 0px; transform: translateY(0px); left: 0px; right: 0px;" data-booted="true"><div class="v-toolbar__content" style="height: 90px;"> <section class="container"><div class="row"><div class="col-6"> <a href="/" class="router-link-active"><div role="img" aria-label="Vuetify Logo" class="v-responsive v-image shrink mr-2" style="width: 120px;"><div class="v-responsive__sizer" style="padding-bottom: 43.0769%;"></div><div class="v-image__image v-image__image--contain" style="background-image: url(&quot;https://flibo-images.s3-us-west-2.amazonaws.com/logos/flibo-logo.svg&quot;); background-position: center center;"></div><div class="v-responsive__content" style="width: 130px;"></div></div> </a></div><div align="right" class="col-6"><a href="https://play.google.com/store/apps/details?id=com.pivot.flibo&amp;referrer=utm_source%3Dflibo-blogs" target="_blank" class="f-primary download-btn v-btn v-btn--contained theme--light v-size--large"><span class="v-btn__content"><span class="mr-2">Download App</span></span></a></div></div> </section></div> </header> <main class="v-content" style="padding: 90px 0px 0px;" data-booted="true"><div class="v-content__wrap"><div <data_hash_2>="" id="article_container"><div <data_hash_1>="" <data_hash_2>=""> <section <data_hash_1>="" class="container"><div <data_hash_1>="" class="row"><div <data_hash_1>="" class="col-12"><ul <data_hash_1>="" class="v-breadcrumbs theme--light"><li><a href="/" class="v-breadcrumbs__item">Home</a></li><li class="v-breadcrumbs__divider">/</li><li><a href="/{contents}-like-{page_slug}" class="v-breadcrumbs__item v-breadcrumbs__item--disabled">{content_types} like {content_title}</a></li></ul><div <data_hash_1>="" aria-label="" class="v-responsive v-image article-movie-poster"><div class="v-responsive__sizer" style="padding-bottom: 50%;"></div><div class="v-image__image v-image__image--preload v-image__image--cover" style="background-position: center center;"></div><div class="v-image__image v-image__image--cover fade-transition-enter-active fade-transition-enter-to" style="background-image: url(&quot;{page_cover}&quot;); background-position: center center;"></div><div class="v-responsive__content"></div></div></div></div><div <data_hash_1>="" class="row"><div <data_hash_1>="" class="col-12"><div <data_hash_1>="" class="article-similar-container"><h1 <data_hash_1>=""> Top 10 awesome {contents} like {content_title} that you will enjoy watching</h1><p <data_hash_1>=""> You just finished watching {content_title} and you can't get over how good this {content_type} was. Now you want to watch more of such masterpieces. We have curated a list of similar {contents} which are created by the likes of <span <data_hash_1>="">{page_artists}</span> . Here goes the list -</p><ol <data_hash_1>=""><div <data_hash_1>="" class="row"><div <data_hash_1>="" class="col-6"><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li></div><div <data_hash_1>="" class="col-6"><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li><li <data_hash_1>=""> {similar_content_list_title}</li></div></div></ol><div <data_hash_1>="" class="row" style="justify-content: center;"><div <data_hash_1>="" class="col-md-12" style="text-align: center;"> <img <data_hash_1>="" data-src="/img/animal-review-{animal_review}.jpg" alt="animal-review" class="animal-review lazy"><div <data_hash_1>="" align="center"><a <data_hash_1>="" href="https://play.google.com/store/apps/details?id=com.pivot.flibo&amp;referrer=utm_source%3Dflibo-blogs" target="_blank" class="f-primary download-btn v-btn v-btn--contained theme--light v-size--large"><span class="v-btn__content"><span <data_hash_1>="" class="mr-2">Download App</span></span></a></div></div></div><ol <data_hash_1>="" class="movie-list"> {similar_content_elements}</ol></div><div <data_hash_1>="" class="row"><div <data_hash_1>="" class="col-md-12 flibo-ad"><a <data_hash_1>="" href="https://play.google.com/store/apps/details?id=com.pivot.flibo&amp;referrer=utm_source%3Dflibo-blogs" target="_blank"><img <data_hash_1>="" data-src="/img/flibo-ad.<img_flibo_ad_hash>.png" alt="Download Flibo app" class="lazy"></a></div></div></div></div> </section></div></div></div> </main></div></div> <script src="/js/chunk-vendors.<js_chunk_vendors_hash>.js"></script><script src="/js/app.<js_app_hash>.js"></script></body></html>
        """.strip()
        similar_content_html = """
        <li <data_hash_1>=""><div <data_hash_1>="" class="row"><div <data_hash_1>="" class="col-md-5 movie-poster-small"><img <data_hash_1>="" data-src="{similar_content_poster}" alt="{similar_content_title}" class="article-poster lazy"></div><div <data_hash_1>="" class="col-md-7"><div <data_hash_1>="" class="movie-content"><h2 <data_hash_1>=""><a <data_hash_1>="" href="https://flibo.ai/content/{similar_content_id}/{similar_content_slug}" target="_blank" style="color: rgb(51, 51, 51); text-decoration: none;">{similar_content_title}</a></h2><p <data_hash_1>="">{similar_content_summary}</p><p <data_hash_1>=""> This {similar_content_type}, created by {similar_content_artists}, scores {similar_content_imdb_score} on IMDb.</p><p <data_hash_1>=""> Genres - {similar_content_genres}</p> {similar_content_streaming_info} {similar_content_trailer}</div></div></div>{swipe_card}</li>
        """.strip()
        swipe_card = """
        <div <data_hash_1>="" class="row" style="justify-content: center;"><div <data_hash_1>="" class="col-md-12" style="text-align: center; margin-top: 16px;"> <img <data_hash_1>="" data-src="/img/swipe-screenshot.<img_swipe_screenshot_hash>.webp" alt="swipe-card" class="animal-review lazy"><div <data_hash_1>="" align="center"><a <data_hash_1>="" href="https://play.google.com/store/apps/details?id=com.pivot.flibo&amp;referrer=utm_source%3Dflibo-blogs" target="_blank" class="f-primary download-btn v-btn v-btn--contained theme--light v-size--large"><span class="v-btn__content"><span <data_hash_1>="" class="mr-2">Download App</span></span></a></div></div></div>
        """.strip()

        page_html = page_html.replace('{contents}', f'{content_type}s')
        page_html = page_html.replace('{content_title}', content['title'])
        page_html = page_html.replace('{content_type}', content_type)
        page_html = page_html.replace('{content_types}', f'{content_type}s'.title())
        page_html = page_html.replace('{page_slug}', content['url_title'])
        if len(content['main_artists']):
            page_html = page_html.replace(
                '{page_artists}',
                ('' if len(content['main_artists']) < 2 else ' and ').join([', '.join(content['main_artists'][0:-1]), content['main_artists'][-1]])
            )
        else:
            page_html = page_html.replace('{page_artists}', 'awesome filmmakers')
        page_html = page_html.replace('{page_cover}', content['cover'].replace('/w500/', '/w780/').replace('/original/', '/w780/'))

        similar_content_elements = []
        for similar_content_id in content['similar_content'][1:11]:
            similar_content = df_contents_info[df_contents_info['content_id'] == similar_content_id].to_dict(orient='records')[0]
            similar_content_type = 'movie' if similar_content['type'] == 'movie' else 'show'

            page_html = re.sub('\{similar_content_list_title\}', similar_content['title'], page_html, 1)

            current_similar_content_html = similar_content_html
            current_similar_content_html = current_similar_content_html.replace('{similar_content_poster}', similar_content['poster'])
            current_similar_content_html = current_similar_content_html.replace('{similar_content_title}', similar_content['title'])
            current_similar_content_html = current_similar_content_html.replace('{similar_content_id}', str(similar_content['content_id']))
            current_similar_content_html = current_similar_content_html.replace('{similar_content_slug}', similar_content['url_title'])
            current_similar_content_html = current_similar_content_html.replace(
                '{similar_content_summary}',
                similar_content['summary_text'] if similar_content['summary_text'] else ''
            )
            current_similar_content_html = current_similar_content_html.replace('{similar_content_type}', similar_content_type)
            if len(similar_content['main_artists']):
                current_similar_content_html = current_similar_content_html.replace(
                    '{similar_content_artists}',
                    ('' if len(similar_content['main_artists']) < 2 else ' and ').join(
                        [', '.join(similar_content['main_artists'][0:-1]), similar_content['main_artists'][-1]]
                    )
                )
            else:
                current_similar_content_html = current_similar_content_html.replace('{similar_content_artists}', 'awesome filmmakers')
            current_similar_content_html = current_similar_content_html.replace('{similar_content_imdb_score}', str(similar_content['imdb_score']))
            current_similar_content_html = current_similar_content_html.replace('{similar_content_genres}', ' | '.join(similar_content['genres']))
            current_similar_content_html = current_similar_content_html.replace('{similar_content_poster}', similar_content['poster'])
            current_similar_content_html = current_similar_content_html.replace('{similar_content_poster}', similar_content['poster'])

            if similar_content['where_to_watch']:
                options = [
                    f"""
                    <span <data_hash_1>="">{'{sep}'}<a <data_hash_1>="" href="{url}" target="_blank" style="font-weight: bold; color: rgb(51, 51, 51); text-decoration: none;">{platform.replace('_', ' ').title()}</a></span>
                    """.strip() for platform, url in similar_content['where_to_watch'].items()
                ]
                for j in range(len(options)):
                    if j == 0:
                        options[j] = options[j].replace('{sep}', '')
                    elif j == len(options) - 1:
                        options[j] = options[j].replace('{sep}', '<span <data_hash_1>="" style="white-space: pre-wrap;"> and </span>')
                    else:
                        options[j] = options[j].replace('{sep}', '<span <data_hash_1>="">, </span>')
                options = ''.join(options).strip()
                streaming_info = f"""
                <p <data_hash_1>=""><span <data_hash_1>="" style="white-space: pre-wrap;">You can watch this on </span>{options}.</p>
                """.strip()
            else:
                streaming_info = ''

            current_similar_content_html = current_similar_content_html.replace('{similar_content_streaming_info}', streaming_info)

            if similar_content['youtube_trailer_id']:
                similar_content_trailer = f"""
                <a <data_hash_1>="" href="https://www.youtube.com/watch?v={similar_content['youtube_trailer_id']}" target="_blank" class="v-btn v-btn--contained theme--light v-size--default" style="text-decoration: none;"><span class="v-btn__content"> Watch Trailer </span></a>
                """.strip()
            else:
                similar_content_trailer = ''

            current_similar_content_html = current_similar_content_html.replace('{similar_content_trailer}', similar_content_trailer)

            if content['similar_content'][1:11].index(similar_content_id) == 2:
                current_similar_content_html = current_similar_content_html.replace('{swipe_card}', swipe_card)
            else:
                current_similar_content_html = current_similar_content_html.replace('{swipe_card}', '')

            similar_content_elements.append(current_similar_content_html)

        page_html = page_html.replace('{similar_content_elements}', ''.join(similar_content_elements))
        page_html = page_html.replace('<data_hash_1>', config['build_hashes']['data_1'])
        page_html = page_html.replace('<data_hash_2>', config['build_hashes']['data_2'])
        page_html = page_html.replace('<js_app_hash>', config['build_hashes']['js']['app'])
        page_html = page_html.replace('<js_home_hash>', config['build_hashes']['js']['home'])
        page_html = page_html.replace('<js_article_hash>', config['build_hashes']['js']['article'])
        page_html = page_html.replace('<js_article_on_demand_hash>', config['build_hashes']['js']['article_on_demand'])
        page_html = page_html.replace('<js_chunk_vendors_hash>', config['build_hashes']['js']['chunk_vendors'])
        page_html = page_html.replace('<css_app_hash>', config['build_hashes']['css']['app'])
        page_html = page_html.replace('<css_home_hash>', config['build_hashes']['css']['home'])
        page_html = page_html.replace('<css_article_hash>', config['build_hashes']['css']['article'])
        page_html = page_html.replace('<css_article_on_demand_hash>', config['build_hashes']['css']['article_on_demand'])
        page_html = page_html.replace('<css_chunk_vendors_hash>', config['build_hashes']['css']['chunk_vendors'])
        page_html = page_html.replace('<img_flibo_ad_hash>', config['build_hashes']['img']['flibo_ad'])
        page_html = page_html.replace('<img_swipe_screenshot_hash>', config['build_hashes']['img']['swipe_screenshot'])
        page_html = page_html.replace('{animal_review}', random.choice(config['build_hashes']['img']['animal_reviews']))

        try:
            with open(f"{config['prerendered_htmls_directory']}{content_type}s-like-{content['url_title']}.html", 'w') as f:
                f.write(page_html)
                f.close()
        except Exception as e:
            print('\nError -', e)
            print(f"{config['prerendered_htmls_directory']}{content_type}s-like-{content['url_title']}.html\n")

    else:
        if i % 100 == 0:
            print(i, f"Skipped {content_type}s-like-{content['url_title']}")
