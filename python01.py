import pandas as pd
import matplotlib.pyplot as plt

# 日本語ラベルを表示するためのフォント設定
plt.rcParams["font.family"] = "Hiragino Sans"
# 負の数のマイナス記号を正しく表示させる設定
plt.rcParams["axes.unicode_minus"] = False

# CSVファイルのパス
csv_path = "kobe.csv"

# ──────── 読み込み ────────
# 1行目：ダウンロード時刻
# 2行目：空行
# 3行目：説明行（列名ではない）
# 4行目：実際の列名（"年月日","平均気温(℃)", "平均気温(℃).1", ...）
# 5行目：空行
# 6行目：品質情報の見出し
# ────────────────────────
# 実際のデータ行（年月日～）は 7行目 (0インデックスでは行番号6) から始まる。
# そこで skiprows=[0,1,2,4,5] とし、header=0 で行番号 3（0インデックスでは「実際の列名」）をヘッダーとして読む。
df = pd.read_csv(
    csv_path,
    encoding="shift_jis",
    skiprows=[0, 1, 2, 4, 5],  # 不要行を飛ばす
    header=0
)

# ['年月日', '平均気温(℃)', '平均気温(℃).1', '平均気温(℃).2', '最高気温(℃)', ... ]
# （.1 や .2 が末尾についた列は品質情報などなので今回は使わない）
# ここでは「年月日」と「平均気温(℃)」だけを残します。
df = df[["年月日", "平均気温(℃)"]]

# ──────── 型変換 ────────
# 年月日列を datetime 型に。形式は "YYYY/M/D" 形式なので "%Y/%m/%d" を指定。
df["年月日"] = pd.to_datetime(df["年月日"], format="%Y/%m/%d", errors="coerce")

# 平均気温(℃)は文字列 ⇒ float に変換
df["平均気温(℃)"] = pd.to_numeric(df["平均気温(℃)"], errors="coerce")

# ──────── グラフ描画 ────────
plt.figure(figsize=(12, 6))
plt.plot(df["年月日"], df["平均気温(℃)"], label="平均気温 (℃)", color="orange")
plt.xlabel("日付")
plt.ylabel("気温 (℃)")
plt.title("平均気温の推移")
plt.grid(True)	#グリッド
plt.legend()	#凡例を表示
plt.tight_layout()	#余白を自動調整
plt.show()