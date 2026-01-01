import json
from pathlib import Path
import random
import requests
from bs4 import BeautifulSoup
import uuid

'''
function of the tool: Get picture of specific ghibli movie.
The choosen picture will be the shown to users after some process.
1. Choose a movie randomly.
2. Select one picture randomly and download.

'''
def getOrigPic() -> dict:
    # read possible movie set
    Tool_Path = Path(__file__).resolve().parent
    Json_Path = Tool_Path.parent / "data" / "movieSet.json"
    with open(Json_Path, "r", encoding="utf-8") as f:
        movieSet = json.load(f)

    # choose a movie as solution randomly
    sol_movie = random.choice(movieSet)
    sol_movie_url = sol_movie["pic_url"]

    # get urls of pictures 
    '''
    Our goal picture urls will contain "gallery" by check the source code.
    Each picture will contain two url, one is original picture and the other is a smaller version.
    We only need original version, which is linked in the <a> tag.

    '''
    response = requests.get(sol_movie_url, timeout=30)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    pic_url = []
    for a in soup.find_all("a", href= True):
        href = a["href"]
        if "gallery" in href:
            pic_url.append(href)

    # choose a picture randomly
    prob_pic = random.choice(pic_url)

    # add a new file to save the problem picture
    codeFile_Path = Path(__file__).resolve().parent.parent
    cache_Path = codeFile_Path / "cache"
    cache_id = uuid.uuid4().hex[:8]
    cache_id_Path = cache_Path / cache_id
    cache_id_Path.mkdir(parents = True, exist_ok = True)

    # download picture
    name_prob_pic = "originalPB.jpg"
    prob_pic_response = requests.get(prob_pic, timeout=30)
    prob_pic_response.raise_for_status()
    prob_pic_Path = cache_id_Path / name_prob_pic
    prob_pic_Path.write_bytes(prob_pic_response.content)

    resultAns = {
        "success" : True,
        "cache_id" : cache_id,
        "ans_movie_zh" : sol_movie["name_zh"],
        "ans_movie_en" : sol_movie["name_en"],
        "ans_movie_jp" : sol_movie["name_jp"],
        "cache_id_folder" : str(cache_id_Path),
        "ans_pic_path" : str(prob_pic_Path)
    }

    return resultAns

if __name__ == "__main__":
    result = getOrigPic()
    print(result)
