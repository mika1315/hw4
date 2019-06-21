import csv
import collections


# 修正を容易にするためファイル名を冒頭で定義
NICKNAMES = "pages.txt"
LINKS = "links.txt"

def nicknames_from_file():
    persons = dict()
    nameToID = dict()
    with open(NICKNAMES, 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:
            # 辞書にキーがない場合にのみ、値を追加する
            persons.setdefault(int(row[0]), row[1])
            nameToID.setdefault(row[1], int(row[0]))
    return persons, nameToID


def nameToID_from_dict(name, nameToID):
    if name in nameToID:
        rootID = nameToID[name]
        return rootID
    else:
        print("Not found")


def links_from_file():
    links = dict()
    with open(LINKS, 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:
            links.setdefault(int(row[0]), []).append(int(row[1]))
    return links


def links_from_dict(currentID, links):
    # linksは辞書
    if currentID in links: # links に currentID というキーがあったら link_list を返す
        link_list = links[currentID]
        return link_list
    else: # なかったら空リストを返す
        links[currentID] = []
        return []
    

def bfs(originID, destinationID):
    visited = set()
    queue = collections.deque()

    # step_dict = dict() # ステップ数を格納
    preID_dict = dict() # ルートを格納

    queue.append(originID)  # 現在地を探索候補キューに格納
    visited.add(originID) # 現在地を探索済リストに格納
    preID_dict[originID] = [originID] # 出発地を格納

    links = links_from_file()

    # キューが空になるまで
    while queue:

        vertexID = queue.popleft() # キューから次の探索地点を一つ取り出す 
        # visited.add(vertexID) # 「探索済みリスト」に取り出した地点を格納（ここが現在地点）

        for neighbor in links_from_dict(vertexID, links): # 現在地から次に行けるポイントを調べる
            if neighbor == destinationID:
                preID_dict[neighbor] = preID_dict[vertexID]  + [neighbor]
                return len(preID_dict[neighbor]) - 1, preID_dict[neighbor]

            elif neighbor not in visited:
                preID_dict[neighbor] = preID_dict[vertexID] + [neighbor]
                visited.add(neighbor)
                queue.append(neighbor)
            
    return -1, []


def bfsToEnd(originID):
    visited = []
    queue = collections.deque()

    # step_dict = dict() # ステップ数を格納
    preID_dict = dict() # ルートを格納

    queue.append(originID)  # 現在地を探索候補キューに格納
    visited.append(originID) # 現在地を探索済リストに格納
    preID_dict[originID] = [originID] # 出発地を格納

    links = links_from_file()

    # キューが空になるまで
    while queue:

        vertexID = queue.popleft() # キューから次の探索地点を一つ取り出す 
        # visited.add(vertexID) # 「探索済みリスト」に取り出した地点を格納（ここが現在地点）

        for neighbor in links_from_dict(vertexID, links): # 現在地から次に行けるポイントを調べる

            if neighbor not in visited:
                preID_dict[neighbor] = preID_dict[vertexID] + [neighbor]
                visited.append(neighbor)
                queue.append(neighbor)
    
    thelongestID = vertexID
            
    return thelongestID
                

def print_route(step, route):
    persons, nameToID = nicknames_from_file()

    if step != -1: # 目的地まで到着できたらルートを表示
        for person in route:
            print('ID: ', person, ', Name: ', persons[person], '->')
    else:
        print('Fail!')


def print_shortest_route():
    while True:
        originName = input("origin : ")
        destinationName = input("destination : ")
        persons, nameToID = nicknames_from_file() # nicknames.txt から辞書を生成
        originID = nameToID_from_dict(originName, nameToID) # 出発地の名前からIDを返す
        destinationID = nameToID_from_dict(destinationName, nameToID) # 目的地の名前からIDを返す
        step, route = bfs(originID, destinationID) # 出発地から目的地まで探索する

        print(originName, " >> ", destinationName)
        print(step, "step")
        print_route(step, route) # ルートを表示
    return None


if __name__ == "__main__":
    # print_shortest_route()
    originName = "Google"
    persons, nameToID = nicknames_from_file() # nicknames.txt から辞書を生成
    originID = nameToID_from_dict(originName, nameToID) # 出発地の名前からIDを返す
    print(persons[bfsToEnd(originID)])
    print(bfsToEnd(originID))

    
