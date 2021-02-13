import pandas as pd
import sqlalchemy
import yaml
import os


config = yaml.safe_load(open('config.yml'))

if not os.path.exists(config['sitemaps']['directory']):
    os.makedirs(config['sitemaps']['directory'])

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

print('Dropping duplicate slugs...')
df_main_contents = df_contents_info.drop_duplicates('url_title')

print(f'Datframe size - {df_main_contents.shape[0]}')
i = 0
date = config['sitemaps']['date']
sitemaps_count = (df_main_contents.shape[0] // config['sitemaps']['url_limit']) + (1 if df_main_contents.shape[0] % config['sitemaps']['url_limit'] else 0)
sitemaps = []
for j in range(sitemaps_count):
    df_current = df_main_contents.iloc[j*config['sitemaps']['url_limit']:(j+1)*config['sitemaps']['url_limit'], :]
    urls = []
    for content in df_current.to_dict(orient='records'):
        i += 1
        if content['similar_content']:
            content_type = 'movie' if content['type'] == 'movie' else 'show'
            urls.append(f"""  <url>
    <loc>https://blog.flibo.ai/{content_type}s-like-{content['url_title']}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>yearly</changefreq>
  </url>
""")
            print(j+1, i, f"{content_type}s-like-{content['url_title']}")
        else:
            print(j+1, i, f"Skipped {content_type}s-like-{content['url_title']}")

    if j == 0:
        urls = [
f"""  <url>
    <loc>https://blog.flibo.ai/</loc>
    <lastmod>{date}</lastmod>
    <changefreq>yearly</changefreq>
  </url>
"""
        ] + urls
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {''.join(urls).strip()}
</urlset>
"""
    with open(f"{config['sitemaps']['directory']}sitemap{j+1}.xml", 'w') as f:
        f.write(sitemap)
        f.close()

    sitemaps.append(f"""    <sitemap>
      <loc>https://blog.flibo.ai/sitemap{j+1}.xml</loc>
    </sitemap>
""")

parent_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
  <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {''.join(sitemaps).strip()}
  </sitemapindex>
"""
with open(f"{config['sitemaps']['directory']}sitemap.xml", 'w') as f:
    f.write(parent_sitemap)
    f.close()
