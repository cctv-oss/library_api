"""
登录接口的自动化测试 —— 你的第一个 pytest 测试文件。

先搞清楚一件事:什么是"自动化测试"?
就是你以前在 Swagger 里用手点按钮测接口的那些动作,
现在用代码写下来,让机器替你反复跑。

一个测试函数,永远只有三步(记缩写 AAA):
    Arrange   准备数据(比如要发的账号密码)
    Act       执行动作(发请求)
    Assert    断言结果(检查返回对不对)
"""
import requests

# 被测后端地址(你本地跑着的服务)
BASE_URL = "http://127.0.0.1:8000"


def test_admin_login_success():
    """用例1:正确的管理员账号密码 -> 应返回 200 和一张 token"""
    # Arrange + Act:直接发一个登录请求
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "account": "admin",
        "password": "admin123",
        "role": "admin",
    })

    # Assert:断言三条
    assert resp.status_code == 200              # ① 状态码是 200
    data = resp.json()
    assert data["token"] != ""                  # ② 拿到 token(门票)了
    assert data["role"] == "admin"              # ③ 身份是管理员


def test_admin_login_wrong_password():
    """用例2:密码错了 -> 应返回 401,并提示"用户名或密码错误"""
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "account": "admin",
        "password": "wrong-password",
        "role": "admin",
    })

    assert resp.status_code == 401
    assert resp.json()["detail"] == "用户名或密码错误"


def test_reader_login_success():
    """用例3:正确的读者(手机号)登录 -> 应返回 200,身份是 reader"""
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "account": "13800000001",
        "password": "123456",
        "role": "reader",
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "reader"


def test_login_invalid_role():
    """用例4:角色传了个不存在的值 -> 应返回 400"""
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "account": "admin",
        "password": "admin123",
        "role": "boss",   # 只允许 admin / reader
    })

    assert resp.status_code == 400


def test_login_missing_password():
    """用例5:干脆不传密码字段 -> 应返回 422(参数校验不通过)"""
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "account": "admin",
        "role": "admin",
        # 注意:这里故意不传 password
    })

    assert resp.status_code == 422
