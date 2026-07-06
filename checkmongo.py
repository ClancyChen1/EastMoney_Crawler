#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 MongoDB 是否启动的脚本（修复 pymongo 版本兼容问题）
"""
import pymongo
import socket
# 核心修复：兼容不同版本的 pymongo 异常类
from pymongo.errors import ConnectionFailure, ConfigurationError
try:
    from pymongo.errors import AuthenticationError
except ImportError:
    try:
        from pymongo.errors import MongoAuthenticationError as AuthenticationError
    except ImportError:
        AuthenticationError = pymongo.errors.PyMongoError

def check_mongodb_status(host="127.0.0.1", port=27017, username=None, password=None, timeout=5):
    """
    验证 MongoDB 是否启动并可正常连接
    :param host: MongoDB 主机地址（默认本地）
    :param port: MongoDB 端口（默认27017）
    :param username: 认证用户名（无则传None）
    :param password: 认证密码（无则传None）
    :param timeout: 连接超时时间（秒）
    :return: 元组 (是否成功, 提示信息)
    """
    # 第一步：先检测端口是否开放（快速判断服务是否启动）
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result != 0:
            return (False, f"❌ MongoDB 端口 {host}:{port} 未开放，服务大概率未启动！")
    except Exception as e:
        return (False, f"❌ 检测端口失败：{str(e)}")

    # 第二步：尝试连接 MongoDB 并执行简单命令（验证服务是否正常响应）
    try:
        # 构建客户端连接
        client_kwargs = {
            "host": host,
            "port": port,
            "serverSelectionTimeoutMS": timeout * 1000  # 超时时间（毫秒）
        }
        # 如果有认证信息，添加到连接参数
        if username and password:
            client_kwargs["username"] = username
            client_kwargs["password"] = password

        client = pymongo.MongoClient(**client_kwargs)

        # 执行简单命令，验证服务是否正常（list_database_names 会触发服务器交互）
        db_list = client.list_database_names()
        # 获取 MongoDB 服务器版本（可选，增强信息）
        server_info = client.server_info()
        version = server_info.get("version", "未知版本")

        # 连接成功，返回详细信息
        success_msg = (
            f"✅ MongoDB 连接成功！\n"
            f"  - 服务器地址：{host}:{port}\n"
            f"  - MongoDB 版本：{version}\n"
            f"  - 可用数据库列表：{db_list[:5]}...（共{len(db_list)}个）"  # 只显示前5个，避免过长
        )
        return (True, success_msg)

    except ConnectionFailure:
        return (False, f"❌ 连接 MongoDB 失败：服务已启动但拒绝连接（可能是配置错误/权限问题）！")
    except AuthenticationError:
        return (False, f"❌ 认证失败：用户名/密码错误！")
    except ConfigurationError:
        return (False, f"❌ 配置错误：请检查主机/端口是否正确！")
    except Exception as e:
        return (False, f"❌ 未知错误：{str(e)}")

if __name__ == "__main__":
    # 配置 MongoDB 连接参数（新手默认无需修改）
    MONGODB_HOST = "127.0.0.1"
    MONGODB_PORT = 27017
    MONGODB_USER = None  # 无认证则留空
    MONGODB_PWD = None   # 无认证则留空

    # 执行验证
    print("="*50)
    print("开始验证 MongoDB 状态...")
    print(f"验证目标：{MONGODB_HOST}:{MONGODB_PORT}")
    print("="*50)
    is_success, msg = check_mongodb_status(
        host=MONGODB_HOST,
        port=MONGODB_PORT,
        username=MONGODB_USER,
        password=MONGODB_PWD
    )

    # 输出结果
    print(msg)
    print("="*50)

    # 失败时给出针对性解决建议
    if not is_success:
        print("\n📌 解决建议：")
        if "端口未开放" in msg:
            print("  1. 检查 MongoDB 服务是否启动（Windows：services.msc 找 MongoDB Server）；")
            print("  2. 确认端口 27017 未被其他程序占用；")
            print("  3. 手动启动：mongod --dbpath 你的数据目录（如 D:\\MongoDB\\data\\db）。")
        elif "认证失败" in msg:
            print("  1. 检查用户名/密码是否正确；")
            print("  2. 若未配置认证，将 MONGODB_USER/MONGODB_PWD 设为 None。")
        else:
            print("  1. 重启 MongoDB 服务；")
            print("  2. 检查防火墙是否阻止 27017 端口；")
            print("  3. 确认 MongoDB 配置文件无错误。")