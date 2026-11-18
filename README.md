# 接口自动化测试框架

[![API Test](https://github.com/Viviana0721/api-autotest-framework/actions/workflows/api-test.yml/badge.svg)](https://github.com/Viviana0721/api-autotest-framework/actions/workflows/api-test.yml)

基于 **Python + Requests + pytest + YAML 数据驱动** 的接口自动化框架，用于演示分层设计、登录态管理与持续集成。

## 目录结构

```
api-autotest-framework/
├── api/                  # 接口层：只封装业务语义，不写 HTTP 细节
│   ├── base_api.py       # 统一请求入口（base_url、超时、日志、Session）
│   └── post_api.py       # 资源接口（posts 模块）
├── testcases/            # 用例层：只关心调接口、传参、断言
│   ├── conftest.py       # 全局 fixture：配置加载、Session、接口实例
│   └── test_post_api.py  # 正向 / 反向 / 数据驱动用例
├── data/                 # 测试数据，与代码分离
│   └── post_cases.yaml
├── config/               # 环境配置，切换环境只改这里
│   └── config.yaml
├── utils/                # 通用工具
│   └── assert_util.py    # 断言封装，统一失败信息
├── pytest.ini
└── requirements.txt
```

## 运行

```bash
pip install -r requirements.txt
pytest              # 全量执行
pytest -k create    # 只跑创建相关用例
pytest -m smoke     # 按标记筛选（预留）
```

## 设计说明

**为什么分三层**
接口层只负责「这个业务怎么调」，用例层只负责「调完断什么」。服务端改字段时只动接口层，用例层不受影响。

**登录态怎么管理**
`conftest.py` 里用 session 级 `requests.Session` 管理，整个测试会话只登录一次，后续请求自动携带 Cookie/Token，避免每个用例重复登录导致用例变慢、状态互相污染。

**数据驱动怎么落地**
查询场景写在 `data/post_cases.yaml`，新增一条场景只加一行数据，不改代码。

**断言为什么单独封装**
失败时要能直接看出「期望什么、实际什么、响应体是什么」，否则排查成本高于写用例成本。

## 已发现的问题

| 编号 | 现象 | 预期 | 实际 | 结论 |
|---|---|---|---|---|
| BUG-01 | 创建资源时缺少必填字段 `title` | 返回 400 并提示字段缺失 | 返回 201 并创建成功 | 服务端缺少入参校验，已用 `xfail(strict=True)` 标记，修复后用例会自动转为失败提醒更新状态 |

## 后续计划

- [ ] 接入真实业务接口后补充幂等用例（`X-Request-Id` 重复提交只建单一次）
- [ ] 集成 Allure 报告（请求响应快照 + 失败堆栈）
- [ ] 用环境变量注入 token，替换写死的测试账号
