from auth import get_token
from fetch import download_all
from assemble import assemble

def main():
    token = get_token()
    #download_all(token)
    assemble()


if __name__ == '__main__':
    main()
