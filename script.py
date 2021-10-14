import re, os, time, requests


def main():
    path = os.path.dirname(os.path.realpath(__file__)) # get ignored links
    skip_comments = ""
    done_path = path + "\\done.txt"
    error_path = path + "\\error.txt"
    for file in [ done_path, error_path ]:
        if os.path.isfile(file):
            with open(file, "r") as f:
                skip_comments += f.read()

    comments = [] # get links from .html
    comments_path = path + "\\comments\\"
    for file in next(os.walk(comments_path), (None, None, []))[2]:
        with open(comments_path + file, "r") as f:
            for link in re.findall("<a href=\"(.*)\">", f.read()):
                if not link in skip_comments:
                    comments.append(link)
    
    if len(comments) > 0:
        print(len(comments), "comments loaded")
        success, errors = 0, 0
        token = input("enter your token: ")

        for num, link in enumerate(comments):
            timer = time.time()
            response = requests.get("https://api.vk.com/method/wall.deleteComment?owner_id={}&comment_id={}&access_token={}&v=5.131".format(*re.findall("https://vk.com/wall(.*)_\d+\?reply=(\d+)", link)[0], token))
            if response.status_code == 200:
                if response.text == "{\"response\":1}":
                    with open(done_path, "a") as f:
                        f.write(link + "\n")
                    success += 1
                elif response.json()["error"]:
                    with open(error_path, "a") as f:
                        f.write(link + "\n")
                        errors += 1

            os.system('cls||clear')
            print("{}/{} processed | {} success | {} errors".format(num + 1, len(comments), success, errors))

            time_passed = time.time() - timer
            if time_passed < 0.34: # api limit 3 rps
                time.sleep(0.34 - time_passed)
        
        print("done!")
    else:
        print("no comments left")

    input("press enter for exit...")


if __name__ == "__main__":
    main()