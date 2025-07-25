import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# 안전하게 절대경로로 지정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '..', 'data', 'df_suwon_flask.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        return render_template('filtered.html', pie_labels=[], pie_values=[], table_data=[], selected=None, routes=[], error_msg=f'CSV 파일을 읽을 수 없습니다: {e}')
    if df.empty:
        return render_template('filtered.html', pie_labels=[], pie_values=[], table_data=[], selected=None, routes=[], error_msg='CSV 데이터가 비어 있습니다.')
    routes = df['노선'].unique().tolist()
    if request.method == 'GET':
        return render_template('filtered.html', routes=routes, selected=None, pie_labels=[], pie_values=[], table_data=[], error_msg=None)
    selected = request.form.get('route')
    if not selected:
        return render_template('filtered.html', routes=routes, selected=None, pie_labels=[], pie_values=[], table_data=[], error_msg='노선을 선택해주세요.')
    filtered_df = df[df['노선'] == selected]
    if filtered_df.empty:
        return render_template('filtered.html', routes=routes, selected=selected, pie_labels=[], pie_values=[], table_data=[], error_msg='해당 노선 데이터가 없습니다.')
    # 시간대별 상위 5개 추출 (예시)
    top5 = filtered_df.groupby('시간대')['이용객수'].sum().nlargest(5)
    pie_labels = top5.index.tolist()
    pie_values = top5.values.tolist()
    table_data = top5.reset_index().to_dict(orient='records')
    return render_template('filtered.html', routes=routes, selected=selected, pie_labels=pie_labels, pie_values=pie_values, table_data=table_data, error_msg=None)

if __name__ == '__main__':
    app.run(debug=True)