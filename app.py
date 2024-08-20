
from flask import Flask, render_template, request
import pandas as pd
import os
from pathlib import Path
app = Flask(__name__, static_folder='static', template_folder='templates')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
@app.route('/')
def home():

    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/brain_disorders')
def brain_disorders():
    # 读取 CSV 文件
    file_path = os.path.join(BASE_DIR, 'static', 'signif_genesCellToDisorderfdr.txt')

    if not os.path.exists(file_path):
        return "CSV does not exist", 404

    data = pd.read_table(file_path)

    # 获取列名和数据
    columns = data.columns.tolist()
    rows = data.values.tolist()

    # 渲染包含表格的页面
    return render_template('brain_disorders.html', columns=columns, data=rows)

@app.route('/IDP')
def IDP():
    # 读取 CSV 文件
    file_path = os.path.join(BASE_DIR, 'static', 'signif_genesCellToIDPfdr.txt')

    if not os.path.exists(file_path):
        return "CSV does not exist", 404

    data = pd.read_table(file_path)

    # 获取列名和数据
    columns = data.columns.tolist()
    rows = data.values.tolist()

    # 渲染包含表格的页面
    return render_template('IDP.html', columns=columns, data=rows)



@app.route('/search_results', methods=['POST'])
def search_results():
    # Get form data

    # 构建csv文件的绝对路径
    result = request.form.get('result')
    cell_type = request.form.get('cell_type')
    keyword = request.form.get('keyword')
    print(result)
    print(str(keyword))
    print(cell_type)
    # Load the CSV files (replace 'file1.csv' and 'file2.csv' with your actual file paths)

    DB_cell = os.path.join(BASE_DIR, 'static', 'signif_genesCellToDisorderfdr.txt')
    IDP_cell = os.path.join(BASE_DIR, 'static', 'signif_genesCellToIDPfdr.txt')
    print(DB_cell)
    # 检查文件是否存在
    if not os.path.exists(DB_cell) or not os.path.exists(IDP_cell):
        return "CSV 文件不存在", 404
    DB_cell = pd.read_table(DB_cell)
    IDP_cell = pd.read_table(IDP_cell)
    if result=='idp':
        filte_data=IDP_cell
    else:
        filte_data = DB_cell
    # Filter the data based on the form inputs (adjust filtering logic as needed)
   # print(filte_data)
    filtered_data= filte_data[(filte_data['pheno'] == str(keyword)) & (filte_data['tissue'] == str(cell_type))]

    # Combine or process the data as needed
    # For example, merging the two datasets
  #  merged_data = pd.merge(filtered_data1, filtered_data2, on='CommonColumn')

    # Convert the DataFrame to HTML
    table_html = filtered_data.to_html(classes='data', header="true", index=False)

    # Render the results page with the table
    return render_template('results.html', table=table_html)
if __name__ == '__main__':
    app.run(debug=True)
