rsync -avz --filter=':- .gitignore' . pi@192.168.1.57:magic-carpet/
ssh -t pi@192.168.1.57 "cd magic-carpet && python3 play.py"
