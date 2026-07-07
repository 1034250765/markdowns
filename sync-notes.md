---
name: sync-notes
description: 将笔记中的绝对图片路径转为相对路径，复制图片到各目录 images/，然后提交并推送到 GitHub
---

# Sync Notes — 笔记同步到 GitHub

将本地 Typora 笔记中的绝对图片路径转换为相对路径，确保图片存放在对应目录的 `images/` 子目录下，最后提交推送到远程仓库。

## 前置条件

- Git 仓库已配置 origin（远程为 `https://github.com/1034250765/markdowns`）
- Typora 图片源目录：`C:\Users\LYX10\AppData\Roaming\Typora\typora-user-images\`
- 笔记目录结构：`FASTapi/`, `python/`, `其他/`, `动手学深度学习/`, `牛只数据集/`

## 操作步骤

### 1. 扫描绝对路径图片

搜索所有 .md 文件中残留的 Typora 绝对路径：

```bash
cd "C:/Users/LYX10/Downloads/Typora"
LC_ALL=en_US.UTF-8 grep -rln "typora-user-images" --include="*.md" .
```

### 2. 提取每个文件引用的图片并按目录分组

为每个含绝对路径的笔记文件，提取其引用的图片文件名，按所在目录去重：

```bash
# 示例：查看 python/claude.md 引用了哪些图片
LC_ALL=en_US.UTF-8 grep -o 'image-[0-9]*\.png' python/claude.md | sort -u
```

### 3. 复制图片到对应目录的 images/

```bash
SRC="C:/Users/LYX10/AppData/Roaming/Typora/typora-user-images"

# 为每个目录分别处理
DST="C:/Users/LYX10/Downloads/Typora/动手学深度学习/images"
mkdir -p "$DST"
cp "$SRC/image-xxx.png" "$DST/"
# ... 逐个复制该目录引用的所有图片
```

### 4. 替换绝对路径为相对路径

路径映射：`C:\Users\LYX10\AppData\Roaming\Typora\typora-user-images\` → `images/`

```bash
cd "C:/Users/LYX10/Downloads/Typora"
find . -name "*.md" -not -path "./.git/*" | while read f; do
  perl -pi -e 's{C:\\\\Users\\\\LYX10\\\\AppData\\\\Roaming\\\\Typora\\\\typora-user-images\\\\}{images/}g' "$f"
done
```

### 5. 检查已有的 ../images/ 引用（旧布局残留）

如果发现笔记中仍有 `../images/` 引用（旧布局，根目录 images 共享），需迁移到每目录布局：

```bash
# 查找残留
LC_ALL=en_US.UTF-8 grep -rln "\.\.\/images/" --include="*.md" .

# 为每个目录从根 images/ 复制所需图片
ROOT_IMG="images"
DST="FASTapi/images"
for img in $(LC_ALL=en_US.UTF-8 grep -roh '../images/image-[0-9]*\.png' FASTapi/ | sed 's|../images/||' | sort -u); do
  cp "$ROOT_IMG/$img" "$DST/"
done

# 替换路径
find . -name "*.md" -not -path "./.git/*" | while read f; do
  perl -pi -e 's{\.\./images/}{images/}g' "$f"
done
```

### 6. 完整性校验

确保没有绝对路径残留，且所有引用的图片都实际存在于对应目录：

```bash
# 检查绝对路径残留（应为 0）
LC_ALL=en_US.UTF-8 grep -r "typora-user-images" --include="*.md" . | wc -l

# 检查 ../images/ 残留（应为 0）
LC_ALL=en_US.UTF-8 grep -r "\.\.\/images/" --include="*.md" . | wc -l

# 检查各目录缺图情况
for dir in FASTapi python 其他 动手学深度学习 牛只数据集; do
  missing=$(comm -23 \
    <(LC_ALL=en_US.UTF-8 grep -roh 'images/image-[0-9]*\.png' "$dir/" 2>/dev/null | sed 's|images/||' | sort -u) \
    <(ls "$dir/images/" 2>/dev/null | sort -u))
  [ -n "$missing" ] && echo "=== $dir 缺图 ===" && echo "$missing"
done
```

### 7. 提交并推送

```bash
git add -A
git status
git commit -m "同步笔记：更新图片路径与内容"
git pull --rebase   # 先拉取远程更新
git push
```

## 路径转换速查表

| 原始路径 | 转换后 | 说明 |
|---------|--------|------|
| `C:\Users\...\typora-user-images\xxx.png` | `images/xxx.png` | 新笔记的绝对路径 |
| `../images/xxx.png` | `images/xxx.png` | 旧布局（根 images） |
| `https://i-blog.csdnimg.cn/...` | 不变 | 网络图片，跳过 |

## 常见遗漏

- **笔记新增图片**：用户可能在批量处理后新增了图片引用，需确认完整性校验通过
- **OneDrive/QQ 等非 Typora 来源图片**：路径不同，需单独处理
- **根 images/ 目录**：迁移到每目录布局后，应删除根 images/ 目录（`git rm -r images/`）
