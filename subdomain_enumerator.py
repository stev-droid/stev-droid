import sys
import requests

i = 1
domain = None
wordlists = None

while i <= len(sys.argv):
    if sys.arg[i] == "-d" and i+1<len(sys.argv):
        domain = sys.argv[i+1]
        i+=2
    elif sys.argv[i] == "-w" and i+1<len(sys.argv):
        with open(sys.argv[i+1],"r") as f:
            wordlists = f.read().splitlines()
        i+=2
    else:
        print("Invalid argument")
        sys.exit(1)
def scan(d0main,word1ists):
    s = requests.Session()
    for word in word1ists:
        try:
            r = s.get(f"https://{word}.{d0main}",timeout=5)
        except requests.ConnectionError:
            continue
        if r.status_code == 200 or r.status_code == 301:
            print(f"Succes:https://{word}.{d0main}")
        else:
            continue

if __name__=="__main__":
    if not wordlists or not domain:
        print("Seems like you forgot flag")
        sys.exit(1)
    scan(domain,wordlists)
