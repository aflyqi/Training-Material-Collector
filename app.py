import os
from flask import Flask, render_template, request, redirect, url_for, session,send_file,flash
from flask_sqlalchemy import SQLAlchemy
import json
# 创建Flask应用
app = Flask(__name__)

# 设置数据库路径，确保数据库存储在 instance 目录下
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'prompts.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# 初始化SQLAlchemy
db = SQLAlchemy(app)

# 创建数据库模型
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String(200), nullable=False)
    output = db.Column(db.String(200), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


# 创建数据库和表
def create_db():
    db_path = os.path.join(app.instance_path, 'prompts.db')
    if not os.path.exists(db_path):
        print(f"创建数据库表...路径：{db_path}")
        db.create_all()  # 创建数据库表
        print("数据库和表已创建！")
    else:
        print("数据库已存在，跳过创建。")


# 首页路由，允许用户提交数据
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['input']
        user_output = request.form['output']
        print(f"接收到的数据: 输入 = {user_input}, 输出 = {user_output}")  # 调试信息
        new_prompt = Prompt(input=user_input, output=user_output)
        db.session.add(new_prompt)
        db.session.commit()
        print("数据已提交到数据库")  # 调试信息
        return redirect(url_for('index'))  # 提交后重定向回首页

    return render_template('index.html')


# 登录页面，管理员登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials, please try again!"
    return render_template('login.html')

# 管理员控制台页面
@app.route('/admin')
def admin_dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # 未登录，重定向到登录页面

    prompts = Prompt.query.all()
    return render_template('admin.html', prompts=prompts)

# 下载prompt数据为txt文件
@app.route('/download_prompts', methods=['GET'])
def download_prompts():
    if 'logged_in' not in session:  # 判断管理员是否已登录
        return redirect(url_for('login'))  # 如果没有登录，跳转到登录页面

    prompts = Prompt.query.all()  # 从数据库获取所有 prompt
    prompt_data = [{"input": prompt.input, "output": prompt.output} for prompt in prompts]  # 构造 JSON 数据

    # 定义要保存的文件路径
    file_path = os.path.join('instance', 'prompts.txt')

    # 将 prompt 数据写入到文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(prompt_data, f, ensure_ascii=False, indent=4)  # 格式化 JSON 数据并写入文件
    except Exception as e:
        return f"Error occurred while writing the file: {str(e)}"

    # 返回文件给用户下载
    return send_file(file_path, as_attachment=True, download_name="prompts.txt")


# 退出登录
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# 应用启动时创建数据库
if __name__ == '__main__':
    # 确保数据库表被创建
    create_db()
    app.run(debug=True)

@app.route('/delete_prompt/<int:prompt_id>', methods=['POST'])
def delete_prompt(prompt_id):
    prompt = Prompt.query.get(prompt_id)
    if prompt:
        db.session.delete(prompt)
        db.session.commit()
        flash('Prompt deleted successfully!', 'success')
    else:
        flash('Prompt not found!', 'error')
    return redirect(url_for('admin_dashboard'))  # 改为 admin_dashboard

