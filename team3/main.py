from flask import Flask, render_template, request
from db import Database  # This imports the Database class
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    db = Database()
    df = db.get_data_as_df()  #Use the new Pandas-enabled method
    db.close()

    if df is None or df.empty:
        return "DB 오류 발생"

    # Extract unique routes
    routes = sorted(df['노선'].dropna().unique())  #Avoid NaN values

    return render_template('base.html', options=routes)

@app.route('/filter', methods=['POST'])
def filter_route():
    selected = request.form.get('route')

    db = Database()
    df = db.get_data_as_df()
    db.close()

    if df is None or df.empty:
        return "DB 오류 발생"

    filtered_df = df[df['노선'] == selected].copy()
    filtered_df['시작시간'] = pd.to_datetime(filtered_df['시작시간'].astype(str), format='%H').dt.time

    grouped = filtered_df.groupby('시작시간')['이용객수'].mean().round()
    top_5 = grouped.sort_values(ascending=False).head(5).sort_index()

    pie_labels = [t.strftime('%H:%M') for t in top_5.index]
    pie_values = top_5.values.tolist()

    #Prepare grouped data for table
    grouped_df = grouped.reset_index().sort_index()
    table_data = grouped_df.to_dict(orient='records')

    return render_template(
        'filtered.html',
        selected=selected,
        table_data=table_data,
        pie_labels=pie_labels,
        pie_values=pie_values
    )


if __name__ == '__main__':
    app.run(debug=True)