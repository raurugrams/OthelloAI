プログラム名：OthelloAI1.0
制作者：raurugrams
プログラム言語：Python3

概要
このソースコードはオセロゲームを実装し、人間とAIが対戦できるようにすることを目的としています。
盤面の状態管理、GUIの表示、AIの実装など、オセロゲームに必要な機能がすべて含まれています。

ソースコード全体の構造
	1. import文
	2. UserAIクラス
	3. OthelloGUIクラス
	4. OthelloBoardクラス
	5. RandomAIクラス
	6. MinimaxAIクラス
	7. MCTSAIクラス
	8. Gameクラス
	9. main関数

1. import文
 必要なライブラリをインポートします。

2. UserAIクラス
 ユーザーがゲームをプレイするためのクラスです。choose_moveメソッドはユーザーが選択した手を返します。

3. OthelloGUIクラス
 tkinterを使用してゲームのグラフィカルユーザーインターフェイス（GUI）を提供するクラスです。

	主なメソッド:
 	 __init__: GUIの初期化と設定
 	 update_display: ゲーム画面の更新
 	 on_closing: ウィンドウが閉じられたときの処理

4. OthelloBoardクラス
 このクラスはオセロの盤面を表現し、ゲームの状態や遷移を管理します。

	主なメソッド:
	__init__: 盤面の初期化
	display: 盤面の表示
	is_valid_move: 手が有効かどうか判定
	get_valid_moves: 有効な手のリストを取得
	has_valid_moves: 有効な手があるかどうか判定
	make_move: 手を適用して盤面を更新
	count_pieces: 石の数をカウント
	get_winner: 勝者を判定
	copy_board: 盤面のコピーを作成
	game_over: ゲームが終了したかどうか判定
	copy: 盤面のディープコピーを作成

5. RandomAIクラス
 ランダムな手を選択するためのAIクラスです。このクラスはchoose_moveメソッドを持ち、ランダムに選択された手を返します。

6. MinimaxAIクラス
 ミニマックスアルゴリズムを使用して手を選択するためのAIクラスです。このクラスはchoose_moveメソッドを持ち、ミニマックスアルゴリズムに基づいて最適な手を選択します。

	主なメソッド:
	__init__: AIの初期化（探索の深さを設定）
	choose_move: ミニマックスアルゴリズムを使用して手を選択
	minimax: 再帰的にミニマックス探索を実行
	evaluate: 盤面の評価関数

7. MCTSAIクラス
 モンテカルロ木探索 (MCTS) アルゴリズムを使用して手を選択するためのAIクラスです。このクラスはchoose_moveメソッドを持ち、MCTSに基づいて最適な手を選択します。

	主なメソッド:

	__init__: AIの初期化（プレイアウト数、探索パラメータを設定）
	choose_move: MCTSを使用して手を選択
	Node: MCTSのノードクラスを定義

8. Gameクラス
 ゲーム全体の管理と進行を行うクラスです。このクラスは盤面とAIを引数にとり、ゲームの進行を制御します。

	主なメソッド:
	__init__: ゲームの初期化
	user_click: ユーザーのクリックイベントを処理
	play: ゲームの進行

9. main関数
 ゲームを実行するためのメイン関数です。この関数では、盤面、AIのインスタンスを作成し、ゲームを開始します。


更新プログラム

v1.1 評価関数の改良とα-β枝刈りの改良:

評価関数を改良するために、盤面の特定の位置に重みを設定します。以下のものは、盤面の各セルの価値を表します。
BOARD_WEIGHTS = [
    [120, -20, 20,  5,  5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20,  5,  5, 20, -20, 120]
]

def evaluate(self, board, player):
    score = 0
    for x in range(board.board_size):
        for y in range(board.board_size):
            if board.board[x][y] == player:
                score += BOARD_WEIGHTS[x][y]
            elif board.board[x][y] == -player:
                score -= BOARD_WEIGHTS[x][y]
    return score

v1.2 ディープラーニングの実装(予定)

