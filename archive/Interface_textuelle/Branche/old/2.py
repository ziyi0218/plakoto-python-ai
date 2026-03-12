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
    """模拟掷两个骰子。"""
    return random.randint(1, 6), random.randint(1, 6)


def afficher_commandes():
    """显示可用命令列表。"""
    print("\nCommandes disponibles :")
    print("  help                      -> 显示命令列表")
    print("  lance                     -> 掷骰子")
    print("  plateau                   -> 显示棋盘")
    print("  move <origine> <destination>  -> 移动一个棋子")
    print("  quit                      -> 退出游戏")


def deplacer_pion(plateau, origine, destination, joueur):
    """
    根据基本规则移动棋子：
      - 检查起始位置是否有当前玩家的棋子；
      - 如果目标位置已有棋子，则判断是否允许移动（目标若被对手超过1个棋子占据，则禁止移动；
        若只有一个对手棋子，则视为封锁，但这里仅打印提示，不做进一步处理）。
    """
    # 检查起始位置是否为空
    if not plateau[origine]:
        print("错误：起始位置为空。")
        return False
    # 检查起始位置的棋子是否属于当前玩家
    if plateau[origine][-1] != joueur:
        print("错误：起始位置的棋子不属于你。")
        return False
    # 检查目标位置
    if plateau[destination]:
        # 若目标位置的棋子不属于当前玩家
        if plateau[destination][-1] != joueur:
            # 如果目标位置有多个对手棋子，则视为封锁，不能移动
            if len(plateau[destination]) > 1:
                print("错误：目标位置被对手封锁。")
                return False
            elif len(plateau[destination]) == 1:
                print("提示：封锁了一个对手棋子。")
                # 这里可扩展封锁逻辑（例如将对手棋子移回起始位置），目前仅打印提示
    # 执行移动：从起始位置移除一个棋子，加入到目标位置
    piece = plateau[origine].pop()
    plateau[destination].append(piece)
    return True


def gestion_commande(cmd, plateau, joueur):
    """
    解析并处理用户输入的命令，
    返回一个元组 (继续游戏的标志, 是否执行了移动操作)。
    """
    if cmd == "help":
        afficher_commandes()
        return True, False
    elif cmd == "lance":
        d1, d2 = lance_de()
        print(f"骰子结果：{d1}, {d2}")
        return True, False
    elif cmd == "plateau":
        afficher_plateau(plateau)
        return True, False
    elif cmd == "quit":
        print("游戏结束，再见！")
        return False, False
    elif cmd.startswith("move"):
        parts = cmd.split()
        if len(parts) != 3:
            print("命令格式错误。正确用法：move <origine> <destination>")
            return True, False
        try:
            # 用户输入的棋盘位置为1~24，这里转换为0~23的索引
            origine = int(parts[1]) - 1
            destination = int(parts[2]) - 1
        except ValueError:
            print("错误：位置必须为数字。")
            return True, False
        if origine < 0 or origine > 23 or destination < 0 or destination > 23:
            print("错误：位置超出范围，请输入1到24之间的数字。")
            return True, False
        if deplacer_pion(plateau, origine, destination, joueur):
            print(f"玩家 {joueur} 移动成功。")
            return True, True
        else:
            print("移动失败。")
            return True, False
    else:
        print("未知命令。请输入 'help' 查看可用命令。")
        return True, False


def main():
    """游戏主循环。"""
    plateau = init_plateau()
    afficher_plateau(plateau)
    afficher_commandes()
    current_player = "B"  # 假设黑棋先行
    print(f"\n轮到玩家 {current_player}。")

    while True:
        cmd = input("\n请输入命令：").strip().lower()
        continuer, move_executed = gestion_commande(cmd, plateau, current_player)
        if not continuer:
            break
        # 如果执行了有效的移动，则切换玩家
        if move_executed:
            current_player = "N" if current_player == "B" else "B"
            print(f"\n轮到玩家 {current_player}。")


if __name__ == "__main__":
    main()

