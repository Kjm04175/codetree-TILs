m, t = list(map(int, input().split()))
r, c = list(map(int, input().split()))
import copy
from heapq import heappop, heappush
pack_map_pos = [r-1, c-1]


dy = [-1, -1, 0, 1, 1, 1, 0, -1]
dx = [0, -1, -1, -1, 0, 1, 1, 1]

monsters = []

def valid(pos):
    y, x = pos
    if 0<= y < 4 and 0<= x < 4:
        return True
    return False

for i in range(m):
    r, c, d =  list(map(int, input().split()))
    monsters.append([r-1, c-1, d-1])


# 동작 전, map에 moster의 위치를 표시해두고 이후 working
# DFS를 통해 3개로 이동했을 때 가능한 모든 경우의 수 (heap에 저장하기)
# 몬스터 시체 관리 (q & life --> 죽은 시간을 입력 후, 제거시간 점검)

# 복제
egg_q = []
corpse_q = []
move_q = []

def copy_monser():
    for i, monster in enumerate(monsters):
        y, x, d = monster
        egg_q.append([y, x, d])


def move_monster():
    maps = [[0 for _ in range(4)] for _ in range(4)]
    py, px = pack_map_pos
    maps[py][px] = 1

    for corpse in corpse_q:
        y, x, t = corpse
        maps[y][x] = 2

    for idx, monster in enumerate(monsters):
        cy, cx, d = monster
        move_y = 0
        move_x = 0
        for i in range(8):
            cd = (d+i)%8

            ny = cy + dy[cd]
            nx = cx + dx[cd]
            if valid([ny, nx]) and maps[ny][nx] == 0:
                move_y = dy[cd]
                move_x = dx[cd]
                d = cd
                break
        if move_x !=0 or move_y!=0:
            monsters[idx] = [cy + move_y, cx + move_x, d]

def DFS(maps, cp, route, depth, eat_nums):
    y, x = cp
    if depth == 3:
        move_q.append([eat_nums, route[0], route[1], route[2]])
    else:
        for idx, (dy, dx) in enumerate([[-1, 0],[0, -1],[1, 0],[0, 1]]):
            ny = y + dy
            nx = x + dx
            if valid([ny, nx]):
                new_map_value = maps[ny][nx]
                maps[ny][nx] = 0
                r = copy.deepcopy(route)
                r.append(idx)
                DFS(maps, [ny, nx], r, depth+1, eat_nums + new_map_value)
                maps[ny][nx] = new_map_value

def move_packman():
    global move_q
    move_q = []
    maps = [[0 for _ in range(4)] for _ in range(4)]

    for monster in monsters:
        y, x, _ = monster
        maps[y][x] += 1

    pos = [pack_map_pos[0], pack_map_pos[1]]
    DFS(maps, pos, [], 0, 0)
    move_q = sorted(move_q, key=lambda x: (-x[0], x[1], x[2], x[3]))
    move_seq = move_q[0]
    move_dir = [[-1, 0],[0, -1],[1, 0],[0, 1]]

    for i in move_seq[1:]:
        pack_map_pos[0] = pack_map_pos[0] + move_dir[i][0]
        pack_map_pos[1] = pack_map_pos[1] + move_dir[i][1]

        for idx, monster in enumerate(monsters):
            if pack_map_pos[0] == monster[0] and pack_map_pos[1] == monster[1]:
                monsters[idx][-1] = -1


def die_monsters(ct):
    global monsters
    monsters = sorted(monsters, key=lambda x:x[-1])
    while (len(monsters)>0 and monsters[0][-1]<0):
        y, x, d = monsters.pop(0)
        heappush(corpse_q, (ct, y, x))

def remove_corpse(ct):
    while len(corpse_q) > 0 and corpse_q[0][0] <= ct+2:
        heappop(corpse_q)

def born():
    global egg_q
    for egg in egg_q:
        monsters.append(egg)
    egg_q = []

for i in range(t):
    copy_monser()
    move_monster()
    move_packman()
    die_monsters(i)
    remove_corpse(i)
    born()
print(len(monsters))