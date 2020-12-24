import random

if __name__ == "__main__":
    node_num = 500
    edge_num = 2500
    fo = open("network2.txt", "w")
    str1 = str(node_num) + " " + str(edge_num) + "\n"
    isFound = {}
    for i in range(edge_num):
        x = random.randint(1, node_num)
        y = random.randint(1, node_num)
        if x not in isFound.keys():
            isFound[x] = [[],[]] # out list, in list, in degree
        if y not in isFound.keys(): 
            isFound[y] = [[],[]]
        if not x==y and y not in isFound[x][0]:
            isFound[x][0].append(y)
            isFound[y][1].append(x)
        else:
            i -= 1

    for i in isFound.keys():
        if isFound[i][0]:
            for j in isFound[i][0]:
                str1 += str(i) + " " + str(j) + " " + str('%.6f' % (1/len(isFound[j][1]))) + "\n"


    fo.write(str1)

    # 关闭文件
    fo.close()