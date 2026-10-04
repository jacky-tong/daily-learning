# Git 的 blob、tree 与 commit：一次提交到底保存了什么？

## 今天学什么

今天只解决一个问题：执行 `git commit` 时，Git 到底保存了什么？

答案不是“把整个文件夹复制一遍”，而是建立一组由哈希连接起来的对象。最重要的三个对象是：

- `blob`：保存文件内容，不保存文件名；
- `tree`：保存文件名、权限，以及它指向的 blob 或子 tree；
- `commit`：指向一次目录快照对应的 tree，同时保存父提交、作者、时间和说明。

## 核心理解

可以把一次提交想成下面这条链：

```text
commit
  ├─ parent → 上一次 commit
  └─ tree   → 本次目录快照
               ├─ README.md → blob
               ├─ app.py    → blob
               └─ src/      → 子 tree
```

因此，分支不需要保存一套文件。分支本质上只需指向某个 commit，而 commit 再沿着 tree 和 blob 找到完整快照。

`git add` 的关键工作是准备内容并更新暂存区；`git commit` 根据暂存区写出 tree，再创建指向该 tree 的 commit。没有进入暂存区的修改不会出现在这次快照里。

### 为什么同样的内容会得到同样的 blob 标识？

传统 SHA-1 仓库会对下面这段字节计算哈希：

```text
blob <内容的字节数>\0<原始内容>
```

文件名不在这段数据里，所以内容相同的两个文件可以引用同一个 blob；文件名由 tree 负责保存。

## 亲手验证

在仓库根目录运行：

```bash
python labs/2026-10-04/git_blob_hash.py README.md
git hash-object README.md
```

两条命令应输出相同的哈希。第一个结果由几十行 Python 直接计算，第二个结果由 Git 计算。

还可以运行内置自测：

```bash
python labs/2026-10-04/git_blob_hash.py --self-test
```

## 自测

1. blob 为什么不需要保存文件名？
2. 两个不同路径的文件内容完全相同时，是否可以指向同一个 blob？
3. commit 直接保存所有文件内容，还是通过 tree 间接找到内容？
4. 为什么修改了工作区文件但没有 `git add`，提交中不会出现这次修改？

<details>
<summary>参考答案</summary>

1. 文件名和目录关系由 tree 保存，blob 只负责内容。
2. 可以，因为 blob 的标识由对象类型、内容长度和内容共同决定，与路径无关。
3. 通过 tree 间接找到 blob 或子 tree。
4. commit 根据暂存区创建 tree，而不是直接读取所有工作区修改。

</details>

## 资料

- [Pro Git：Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects.html)
- [Pro Git：Plumbing and Porcelain](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain.html)
- [git-hash-object 文档](https://git-scm.com/docs/git-hash-object.html)

## 一句话复盘

Git 的提交不是文件夹备份，而是一个 commit 指向 tree、tree 再指向 blob 的可追踪对象图。

