# Codex 偏好建模 Skills

这是一套中文 Codex skills，用来建立、维护和加载长期用户偏好模型。

仓库内只包含可复用的源码，不包含任何真实用户画像、访谈日志或运行态数据。

## 包含内容

- `preference-interview-zh`：多轮访谈，建立偏好模型
- `preference-memory-zh`：根据真实协作中的新信号增量更新偏好
- `preference-bootstrap-zh`：在新会话开始时读取并应用已有偏好模型

## 推荐用法

这套 skills 推荐采用低 token 的默认部署方式：

1. 安装这三个 skill
2. 在全局 `AGENTS.md` 中自动读取 `session-brief.md`
3. 只有在出现新的稳定偏好时，再调用 `preference-memory-zh`
4. 只有首次建模或模型明显过期时，才重新跑完整访谈

可参考 [AGENTS.example.md](./AGENTS.example.md) 和 [USAGE.md](./USAGE.md)。

## 仓库结构

```text
skills/
  preference-bootstrap-zh/
  preference-interview-zh/
  preference-memory-zh/
AGENTS.example.md
USAGE.md
```

## 设计原则

- 访谈通常控制在 `40-80` 题内。
- 总上限约为 `100` 题，除非仍存在会明显影响未来行为的关键歧义。
- 最后 `10-20` 题在需要时可用于补充人格、个性、三观和盲点建模。
- 已经问清的主题不再反复追问近似问题。
- 模型足够清楚后，应更多从真实协作中渐进学习，而不是反复重开长问卷。
- 本地运行态数据存放在用户自己的 Codex 目录之外，不应随仓库提交。
- 最省 token 的默认方式是 `AGENTS.md + session-brief.md`，而不是每次新会话都重跑整套 skills。

安装方式、运行流程和目录说明见 [USAGE.md](./USAGE.md)。
