import csv
import collections

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


def nameToID_from_dict(rootName):
    persons, nameToID = nicknames_from_file()
    rootID = nameToID[rootName]
    return rootID


def links_from_file():
    links = dict()
    with open(LINKS, 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:
            # 辞書にキーがない場合のエラー処理すべきだけど未実装
            links.setdefault(int(row[0]), []).append(int(row[1]))
    return links


def links_from_dict(currentID):
    links = links_from_file()
    link_list = links[currentID]
    return link_list

def bfs(originID, destinationID):
    visited = set()
    queue = collections.deque()

    step_dict = dict() # ステップ数を格納
    preID_dict = dict() # ルートを格納
    step = 0

    queue.append(originID)  # 現在地を探索候補キューに格納
    step_dict[originID] = step # 出発地は 0 step
    preID_dict[originID] = [originID] # 出発地を格納

    # キューが空になるまで
    while queue:

        vertexID = queue.popleft() # キューから次の探索地点を一つ取り出す 
        visited.add(vertexID) # 「探索済みリスト」に取り出した地点を格納（ここが現在地点）
        step = step_dict[vertexID]

        for neighbor in links_from_dict(vertexID): # 現在地から次に行けるポイントを調べる
            if neighbor == destinationID:
                preID_dict[neighbor] = preID_dict[vertexID]  + [neighbor]
                step_dict[neighbor] = step + 1
                return step_dict[neighbor], preID_dict[neighbor]

            elif neighbor not in visited:
                preID_dict[neighbor] = preID_dict[vertexID] + [neighbor]
                step_dict[neighbor] = step + 1
                queue.append(neighbor)
            
    return -1, []
                
def print_root(step, root):
    persons, nameToID = nicknames_from_file()

    if step != -1: # 目的地まで到着できたらルートを表示
        for person in root:
            print('ID: ', person, ', Name: ', persons[person], '->')
    else:
        print('Fail!')



if __name__ == "__main__":
    originName = "jacob" # 出発地
    destinationName = "erik" # 目的地
    originID = nameToID_from_dict(originName) # 出発地の名前からIDを返す
    destinationID = nameToID_from_dict(destinationName) # 目的地の名前からIDを返す
    step, root = bfs(originID, destinationID) # 出発地から目的地まで探索する

    print(originName, ' >> ', destinationName)
    print(step, 'step')
    print_root(step, root) # ルートを表示