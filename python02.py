import pandas as pd
import plotly.express as px

# 日本語ラベルを表示するためにフォント指定は不要（Plotly はフォント埋め込みで対応可能）
# 負の数のマイナス記号も Plotly 側で自動的に正しく表示されます。

# ──────── CSVファイルのパス ────────
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
# そこで skiprows=[0,1,2,4,5] とし、header=0 で行番号3（0インデックスでは「実際の列名」）をヘッダーとして読む。
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

# ──────── インタラクティブ・グラフ描画（Plotly） ────────
# Plotly Express のラインチャートを使い、ホバー時に日付と気温が見えるように設定します。
fig = px.line(
    df,
    x="年月日",
    y="平均気温(℃)",
    title="平均気温の推移",
    labels={
        "年月日": "日付",
        "平均気温(℃)": "平均気温 (℃)"
    }
)

# ホバー表示フォーマットを指定（例：YYYY-MM-DD 形式＋気温表示）
fig.update_traces(
    mode="lines+markers",
    hovertemplate="日付: %{x|%Y-%m-%d}<br>気温: %{y} ℃<extra></extra>"
)

# レイアウト調整（凡例・グリッドなど、必要なら細かく調整可能）
fig.update_layout(
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)

# HTML ファイルとして保存（Plotly.js の CDN を利用してインタラクティブ機能を組み込み）
output_html = "temperature.html"
fig.write_html(output_html, include_plotlyjs="cdn")
print(f"Saved interactive plot to {output_html}")
# テスト用のコメント追加です
