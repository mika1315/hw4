import csv
import collections
import itertools

# 修正を容易にするためファイル名を冒頭で定義
NICKNAMES = "nicknames.txt"
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


def nameToID_from_dict(name, persons, nameToID):
    rootID = nameToID[name]
    return rootID


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

    step_dict = dict() # ステップ数を格納
    preID_dict = dict() # ルートを格納
    step = 0

    queue.append(originID)  # 現在地を探索候補キューに格納
    step_dict[originID] = step # 出発地は 0 step
    preID_dict[originID] = [originID] # 出発地を格納

    links = links_from_file()

    # キューが空になるまで
    while queue:

        vertexID = queue.popleft() # キューから次の探索地点を一つ取り出す 
        visited.add(vertexID) # 「探索済みリスト」に取り出した地点を格納（ここが現在地点）
        step = step_dict[vertexID]

        for neighbor in links_from_dict(vertexID, links): # 現在地から次に行けるポイントを調べる
            if neighbor == destinationID:
                preID_dict[neighbor] = preID_dict[vertexID]  + [neighbor]
                step_dict[neighbor] = step + 1
                return step_dict[neighbor], preID_dict[neighbor]

            elif neighbor not in visited:
                preID_dict[neighbor] = preID_dict[vertexID] + [neighbor]
                step_dict[neighbor] = step + 1
                queue.append(neighbor)
            
    return -1, []
                
def print_route(step, route):
    persons, nameToID = nicknames_from_file()

    if step != -1: # 目的地まで到着できたらルートを表示
        for person in route:
            print('ID: ', person, ', Name: ', persons[person], '->')
    else:
        print('Fail!')


if __name__ == "__main__":
    # originName = "jacob" # 出発地
    # destinationName = "erik" # 目的地
    # persons, nameToID = nicknames_from_file() # nicknames.txt から辞書を生成
    # originID = nameToID_from_dict(originName, persons, nameToID) # 出発地の名前からIDを返す
    # destinationID = nameToID_from_dict(destinationName, persons, nameToID) # 目的地の名前からIDを返す
    # step, route = bfs(originID, destinationID) # 出発地から目的地まで探索する

    # print(originName, " >> ", destinationName)
    # print(step, "step")
    # print_route(step, route) # ルートを表示

    persons, nameToID = nicknames_from_file()
    combi = list(itertools.combinations(range(49), 2)) # 全ての組み合わせを探す
    count = 0

    # print(combi) 
    for (originID, destinationID) in combi:
        step_to, root_to = bfs(originID, destinationID) # 出発地から目的地まで探索する
        step_from, root_from = bfs(destinationID, originID) # 出発地から目的地まで探索する
        # 片思いを探す
        if step_to == -1 and step_from != -1:
            print(persons[destinationID], " is in one-sided love with ", persons[originID])
            count += 1
        elif step_to != -1 and step_from == -1:
            print(persons[originID], " is in one-sided love with ", persons[destinationID])
            count += 1

    print("one-sided couple: ", count)

