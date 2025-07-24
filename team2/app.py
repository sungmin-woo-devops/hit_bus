from flask import Flask, render_template, request
import json
import pandas as pd
from db import Database  # 클래스 불러오기

app = Flask(__name__)

# ✅ 앱 시작 시 한 번만 DB 연결 및 데이터 불러오기
db = Database()
cached_df = db.get_data_as_df()
db.close()

# ✅ 전처리도 캐싱 시점에 수행 후 메모리에 데이터 저장
if cached_df is not None and not cached_df.empty:
    cached_df['이용객수'] = pd.to_numeric(cached_df['이용객수'], errors='coerce')
    cached_df['시작시간'] = pd.to_numeric(cached_df['시작시간'], errors='coerce')
    cached_df['노선'] = cached_df['노선'].astype(str).str.strip()
else:
    cached_df = pd.DataFrame()  # 예외 방지용

@app.route('/', methods=['GET'])
def index():
    df = cached_df.copy()  # ✅ 요청마다 복사본 사용

    if df.empty:
        return "DB에서 데이터를 불러오지 못했습니다."

    top_routes = df['노선'].value_counts().head(4).index.tolist()
    selected_route = request.args.get('route') or top_routes[0]
    filtered_df = df[df['노선'] == selected_route]

    table_html = filtered_df.head(20).to_html(classes='table table-bordered table-sm', index=False)
    grouped = filtered_df.groupby('시작시간')['이용객수'].mean().sort_index()

    chart_labels = list(grouped.index)
    chart_values = list(grouped.values)

    return render_template(
        'index.html',
        table=table_html,
        routes=top_routes,
        selected_route=selected_route,
        chart_labels=json.dumps(chart_labels),
        chart_values=json.dumps(chart_values)
    )

if __name__ == '__main__':
    app.run(debug=True, threaded=True)  # ✅ 멀티스레드 처리도 함께 적용
