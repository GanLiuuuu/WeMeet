from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有域名的跨域请求

@app.route('/connect', methods=['POST'])
def connect():
    data = request.get_json()
    print('连接请求:', data)
    
    # 这里可以处理连接逻辑，例如验证 IP 和端口
    # 假设连接成功
    return jsonify({'message': '连接成功'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # 或者使用 host='127.0.0.1' 仅限本地访问