## 集成git

通过git官网下载git，选择自己的系统下载即可

若是第一次使用 git 的话，请先配置全局的用户名和邮箱

```python
git config --global user.name "Your Name"
git config --global user.email "youremail@yourdomain.com"

git config --list
user.name=Your Name
user.email=youremail@yourdomain.com


# 初始化仓库
git init

# 克隆远程仓库
git clone <repo_url>

# 查看当前状态
git status

# 添加全部修改到暂存区
git add .

# 提交到本地仓库
git commit -m "提交说明"

# 查看提交历史（精简版）
git log --oneline

# 查看文件修改差异
git diff


# 添加远程仓库
git remote add <remote_name> <repo_url>

# 推送本地分支到远程
git push -u <remote_name> <branch_name>
git push [远程仓库名] [本地分支名]:[远程分支名]


# 强制推送（慎用！）
git push -f

# 拉取远程更新
git pull <remote_name> <branch_name>

# 获取远程分支但不合并
git fetch

# 删除远程分支
git push <remote_name> --delete <branch_name>


# 图形化提交历史
git log --graph --all

# 按作者搜索提交
git log --author="name"

# 搜索提交内容
git log -S "keyword"

# 显示某文件的修改历史
git blame <file>

# 忽略文件权限变更
git config core.fileMode false

# 生成.gitignore模板
curl https://gitignore.io/api/<语言/工具>

# 查看仓库大小
git count-objects -vH

# 克隆指定分支（浅克隆）
git clone --branch <branch_name> --depth 1 <repo_url>

```

