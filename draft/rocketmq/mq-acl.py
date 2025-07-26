from flask import Flask, request, jsonify
import docker
import logging
from functools import wraps

app = Flask(__name__)
client = docker.from_env()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except docker.errors.NotFound as e:
            logger.error(f"容器未找到: {str(e)}")
            return jsonify({"status": "error", "message": f"容器未找到: {str(e)}"}), 404
        except docker.errors.APIError as e:
            logger.error(f"Docker API错误: {str(e)}")
            return jsonify({"status": "error", "message": f"Docker API错误: {str(e)}"}), 500
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            return jsonify({"status": "error", "message": f"服务器错误: {str(e)}"}), 500
    return wrapper

@app.route('/api/exec', methods=['POST'])
@handle_errors
def execute_command():
    """
    执行Docker容器命令的API端点
    请求格式:
    {
        "container": "容器名",
        "command": "要执行的命令",
        "user": "root" (可选, 执行用户),
        "workdir": "/path" (可选, 工作目录),
        "environment": {"VAR": "value"} (可选, 环境变量)
    }
    """
    data = request.get_json()
    
    # 验证输入
    if not data or 'container' not in data or 'command' not in data:
        return jsonify({"status": "error", "message": "缺少必要参数: container 和 command"}), 400
    
    container_name = data['container']
    command = data['command']
    
    logger.info(f"执行命令 - 容器: {container_name}, 命令: {command}")
    
    # 获取容器并执行命令
    container = client.containers.get(container_name)
    exit_code, output = container.exec_run(
        cmd=command,
        workdir=data.get('workdir'),
        user=data.get('user'),
        environment=data.get('environment'),
        demux=False,
        tty=False,
        privileged=False
    )
    
    # 返回结果
    result = {
        "status": "success",
        "container": container_name,
        "command": command,
        "exit_code": exit_code,
        "output": output.decode('utf-8') if output else ""
    }
    
    logger.info(f"命令执行完成 - 容器: {container_name}, 退出码: {exit_code}")
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)