SET 

CURRENT_PATH=%0
cd %CURRENT_PATH%

python generate-url-list.py
scrapy crawl inaturalist

cmd /k