from pytrends.request import TrendReq
import pandas as pd

# pytrends = TrendReq(hl='KR', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})
kw_list = ["bts"]
pytrends = TrendReq(hl="ko", tz=540)
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='KR', gprop='')
related_topics = pytrends.related_topics()
# print(related_topics)
# print("-------------")
df = pytrends.related_queries()
df = pd.DataFrame(df["bts"]["rising"])
print(df["query"].values)