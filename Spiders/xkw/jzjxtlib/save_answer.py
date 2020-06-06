def save(answer, title):
    save_file = open("answer_%s.txt" % str(title), "w")
    save_file.write(answer)
    print(save_file.name)
    save_file.close()