import random

def init_plateau():
    """初始化棋盘，放置初始棋子。"""
    plateau = {i: [] for i in range(24)}
    plateau[0] = list("B" * 15)  # 15个黑棋
    plateau[23] = list("N" * 15)  # 15个白棋
    return plateau

def afficher_plateau(plateau):
    """以ASCII形式显示棋盘。"""
    for i in range(24):
        print(f"{i + 1} : {''.join(plateau[i]) if plateau[i] else '-'}")

def lance_de():
    """模拟掷两个骰子，若为对子则返回4次该值，否则返回两个骰子点数。"""
    d1, d2 = random.randint(1,6), random.randint(1,6)
    if d1 == d2:
        return [d1] * 4  # 双骰子：可移动4次
    else:
        return [d1, d2]

def afficher_commandes():
    """显示可用命令列表。"""
    print("\nCommandes disponibles :")
    print("  help                      -> 显示命令列表")
    print("  lance                     -> 掷骰子")
    print("  plateau                   -> 显示棋盘")
    print("  move <origine> <destination>  -> 移动一个棋子")
    print("  quit                      -> 退出游戏")

def is_move_legal_by_dice(origine, destination, dice, joueur):
    """
    根据骰子点数判断移动是否合法。
    假设：
      - 对于黑棋（B），必须从较小索引向较大索引移动，移动距离应等于某个骰子值；
      - 对于白棋（N），则相反，必须从较大索引向较小索引移动。
    """
    move_distance = abs(destination - origine)
    # 检查移动距离是否在骰子列表中
    if move_distance in dice:
        if joueur == "B" and destination > origine:
            return True
        if joueur == "N" and origine > destination:
            return True
    return False

def deplacer_pion(plateau, origine, destination, joueur):
    """
    根据基本规则移动棋子：
      - 检查起始位置是否有当前玩家的棋子；
      - 如果目标位置已有棋子，则判断是否允许移动（若目标被对手超过1个棋子占据，则禁止移动；若只有一个对手棋子，则提示封锁）。
    """
    if not plateau[origine]:
        print("错误：起始位置为空。")
        return False
    if plateau[origine][-1] != joueur:
        print("错误：起始位置的棋子不属于你。")
        return False
    if plateau[destination]:
        if plateau[destination][-1] != joueur:
            if len(plateau[destination]) > 1:
                print("错误：目标位置被对手封锁。")
                return False
            elif len(plateau[destination]) == 1:
                print("提示：封锁了一个对手棋子。")
    piece = plateau[origine].pop()
    plateau[destination].append(piece)
    return True

def gestion_commande(cmd, plateau, joueur, dice):
    """
    解析并处理用户输入的命令，返回元组 (继续游戏标志, 是否执行了移动操作, 当前剩余骰子)
    """
    if cmd == "help":
        afficher_commandes()
        return True, False, dice
    elif cmd == "lance":
        new_dice = lance_de()
        print("骰子结果：", new_dice)
        return True, False, new_dice
    elif cmd == "plateau":
        afficher_plateau(plateau)
        return True, False, dice
    elif cmd == "quit":
        print("游戏结束，再见！")
        return False, False, dice
    elif cmd.startswith("move"):
        parts = cmd.split()
        if len(parts) != 3:
            print("命令格式错误。正确用法：move <origine> <destination>")
            return True, False, dice
        try:
            origine = int(parts[1]) - 1
            destination = int(parts[2]) - 1
        except ValueError:
            print("错误：位置必须为数字。")
            return True, False, dice
        if origine < 0 or origine > 23 or destination < 0 or destination > 23:
            print("错误：位置超出范围，请输入1到24之间的数字。")
            return True, False, dice
        # 检查该移动是否与骰子点数匹配（内部判断，不显示所有可能性）
        if not is_move_legal_by_dice(origine, destination, dice, joueur):
            print("错误：此移动不符合骰子点数或方向要求。")
            return True, False, dice
        # 尝试移动棋子
        if deplacer_pion(plateau, origine, destination, joueur):
            print(f"玩家 {joueur} 移动成功。")
            # 移除一个对应的骰子点数（若有多个相同，则移除第一个）
            move_distance = abs(destination - origine)
            try:
                dice.remove(move_distance)
            except ValueError:
                pass
            return True, True, dice
        else:
            print("移动失败。")
            return True, False, dice
    else:
        print("未知命令。请输入 'help' 查看可用命令。")
        return True, False, dice

def main():
    """文本界面游戏主循环，内部判断合法移动，不展示所有合法移动方案。"""
    plateau = init_plateau()
    afficher_plateau(plateau)
    afficher_commandes()
    current_player = "B"  # 假设黑棋先行
    dice = []  # 回合初始没有骰子
    print(f"\n轮到玩家 {current_player}。")

    while True:
        # 若当前没有骰子，则要求先投骰子
        if not dice:
            print("请先投骰子（输入 'lance'）。")
            cmd = input("\n请输入命令：").strip().lower()
        else:
            cmd = input("\n请输入命令：").strip().lower()

        continuer, move_executed, dice = gestion_commande(cmd, plateau, current_player, dice)
        if not continuer:
            break
        if move_executed:
            # 如果本回合还有剩余骰子，则当前玩家继续移动
            if dice:
                print(f"剩余骰子点数：{dice}")
            else:
                # 所有骰子用完后，切换玩家
                current_player = "N" if current_player == "B" else "B"
                print(f"\n轮到玩家 {current_player}。")
        # 显示当前棋盘状态
        afficher_plateau(plateau)

if __name__ == "__main__":
    main()
