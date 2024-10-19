from bs4 import BeautifulSoup
from requests import get


def get_url(url):
    count = 0
    cont = get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')

    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
        if lst[count - 5] == "/results":
            raise Exception("No Video Found for this Topic!")

    views_count = lst[count - 19]
    time_stamp = lst[count - 29]
    unique_id = lst[count - 5]

    return {
        "video_url": f"https://www.youtube.com{unique_id}",
        "time": time_stamp,
        "views": views_count,
    }


url = f"https://www.youtube.com/results?search_query={"we dont talk anymore"}"

video_open = get_url(url)
print(video_open["video_url"])
print(video_open["time"])
print(video_open["views"])
