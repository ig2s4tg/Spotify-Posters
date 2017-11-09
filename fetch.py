import requests, os
from urllib.request import urlretrieve as urlr

def get_image_url(token, album_name, offset=0, size=0):
    return get_all_image_urls(token, album_name, size)[offset]

def get_all_image_urls(token, album_name, size=0):
    print("token: ", token)
    r = requests.get("http://api.spotify.com/v1/search?q={}&type=album".format(album_name),
        headers={"Authorization": "Bearer {}".format(token)})
    r = r.json()
    print(r)
    r = r["albums"]["items"]
    if len(r) == 0:
        print("no albums found for " + album_name)
    return list(map(lambda x : x.replace("https:","http:"), [i["images"][size]["url"] for i in r]))

def download_image(token, image_url, folder="./img/", file_name=""):
    if file_name == "":
        file_name = image_url.split("/")[-1]
    if not (folder.endswith("/") or folder == ""):
            folder += "/"
    urlr(image_url, folder + file_name)

def download_all(token, input_file="albums.txt", folder="./img/"):
    if not os.path.exists(folder):
        os.mkdir(folder)
    with open(input_file) as f:
        for line in f.readlines():
            name = " ".join(line.split(" ")[:-1])
            offset = 0
            if line.split(" ")[-1] != "0":
                offset = int(line.split(" ")[-1])
            url = get_image_url(token, name, offset, 0)
            download_image(token, url, folder, file_name=name + ".jpg")
