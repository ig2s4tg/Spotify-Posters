import requests, base64, json, time

def is_token_expired(keys=None):
    if not keys:
        with open("keys.json", "r") as k:
            keys = json.load(k)
    return "token_expiration" in keys and keys["token_expiration"] < int(time.time())

def get_token():
    with open("keys.json", "r") as k:
        keys = json.load(k)

    #check the json file for unexpired token
    if "token" not in keys or "token_expiration" not in keys:
        print("Unable to read token key from json file, retrieving another.")
    elif is_token_expired(keys):
        print("Token is expired, retrieving another.")
    else:
        return keys["token"]

    client, secret = keys["client"], keys["secret"]
    #gets the base 64 encoding of client:secret
    b64auth = base64.b64encode(str.encode("{}:{}".format(client, secret)))
    print("Retrieving token...")

    r = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": "Basic {}".format(b64auth.decode("utf-8"))},
        data={"grant_type": "client_credentials"}
    )
    print("Retrieved token.")
    r = r.json()

    keys["token"] = r["access_token"]
    keys["token_expiration"] = r["expires_in"] + int(time.time())

    with open("keys.json", "w") as k:
        json.dump(keys, k)
    print("Stored token locally in keys.json")

    return keys["token"]
