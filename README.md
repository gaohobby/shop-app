# 简易商城

基于 Flask 的简易商城系统，支持管理员商品管理、用户购物车和下单。

## 功能

### 普通用户
- 注册、登录
- 浏览商品、搜索、分页
- 加入购物车、修改数量
- 下单、查看订单

### 管理员
- 添加、编辑、删除商品
- 查看所有订单
- 修改订单状态

## 技术栈

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- Jinja2

## 运行方式

安装依赖：

```bash
pip install flask flask-sqlalchemy flask-login