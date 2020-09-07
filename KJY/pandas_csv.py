import os
import pandas as pd
from datetime import datetime, timedelta
import configparser
import glob

config = configparser.ConfigParser()
#설정파일이 있는경우 설정합니다.
#config.read('/root/crawling/crawler.conf') 

def to_csv(data):

	pathlink ="./"
		    
	# db create
	if not os.path.isdir(pathlink):
		os.mkdir(pathlink)

	present_date = str(datetime.utcnow() + timedelta(hours=9))[:10] #파일명에 날짜구분하기 위한 시간

	# col = ["search", "user_id", "좋아요", "hashtags"]
    
    # CSV파일 생성
	if len(glob.glob(pathlink + "/" + present_date + ".csv")) == 1:
		cnt = len(pd.read_csv(pathlink + "/" + present_date + ".csv", index_col=0).index)
		time_pd = pd.DataFrame(data, index=[cnt])
		time_pd.to_csv(pathlink + "/" + present_date + ".csv", mode='a', header=False, encoding='utf-8-sig')
	else:
		cnt = 0
		time_pd = pd.DataFrame(data, index=[cnt])
		time_pd.to_csv(pathlink + "/" + present_date + ".csv", mode='a', encoding='utf-8-sig')