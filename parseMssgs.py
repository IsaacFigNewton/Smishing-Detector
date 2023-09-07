if __name__ == "__main__":
    inFile = open("chatgpt-spam.txt", "r", encoding="utf-8").readlines()
    outFile = open("chatgpt-spam2.txt", "w", encoding="utf-8")

    for line in inFile:
        if line != "\n":
            outFile.write("spam\t" + line)

