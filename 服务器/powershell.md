# PowerShell 简介

> 在大多数人印象中，Windows 的命令行工具要么是年代久远的 **cmd**，要么是让人头秃的"图形界面点来点去"。但其实，微软早在 2006 年就推出了一款功能强大、专为系统管理员设计的现代命令行工具 —— **PowerShell**。

PowerShell 是微软推出的跨平台（Windows / Linux / macOS）自动化与配置管理框架，由「命令行外壳（host）」和「脚本语言」两部分组成。

PowerShell 基于 .NET（完整 .NET Framework 或 .NET Core / .NET 6+），因此能直接调用数以千计的 .NET API，并原生支持面向对象管道（object pipeline），而非传统 Shell 的纯文本流。

PowerShell 构建在 .NET Framework 之上，专为系统管理员和高级用户设计，用于自动化各种系统管理任务。

### PowerShell 的核心特点

1. **面向对象**：不同于传统命令行工具处理文本，PowerShell 直接处理 .NET 对象
2. **强大的管道功能**：可以轻松地将一个命令的输出传递给另一个命令
3. **可扩展性**：可以创建自定义 cmdlet（命令）和模块
4. **跨平台支持**：PowerShell Core 可在 Windows、Linux 和 macOS 上运行

# PowerShell 核心概念

PowerShell 不只是一个命令行工具，它的设计理念、功能架构和使用方式与传统 Shell 有着显著区别。

------

## 一、Cmdlet：最小命令单元

### 什么是 Cmdlet？

Cmdlet（发音为 *command-let*）是 PowerShell 中最基本的命令单元，它们都是基于 .NET 的类，运行后会返回一个或多个 **.NET 对象**。

### 命名规则：动词-名词

每个 Cmdlet 都遵循 **动词-名词** 命名规范，例如：

| Cmdlet        | 含义                           |
| :------------ | :----------------------------- |
| `Get-Process` | 获取进程信息                   |
| `Set-Item`    | 设置某个资源项的值             |
| `Remove-Item` | 删除文件、注册表项等           |
| `New-User`    | 创建新用户（若安装了 AD 模块） |

PowerShell 附带了数百个 Cmdlet，且第三方模块可以自定义更多。

### 示例

```
Get-Service
Get-ChildItem -Path C:\Windows
```

你也可以使用 `Get-Command` 查看所有可用的 Cmdlet：

```
Get-Command -CommandType Cmdlet
```





## 二、对象管道（Object Pipeline）

### 和 UNIX/Linux 的管道有啥区别？

在传统 Shell 中，管道 (`|`) 传递的是文本字符串。而在 PowerShell 中，**管道传递的是完整的 .NET 对象**。

这就意味着你可以保留结构化数据（属性、方法）进行后续处理。

### 示例：按 CPU 使用率过滤进程

```
Get-Process | Where-Object { $_.CPU -gt 100 } | Select-Object Name, CPU
```

### 管道传值之美

你不需要使用 `awk`、`cut`、`grep` 等工具去"解析"输出，而是直接操作对象属性。



## 三、Provider 和 PSDrive：资源驱动器抽象

PowerShell 提供了一种统一的资源访问方式：**Provider 模型**，它把各种资源映射为虚拟驱动器（PSDrive），就像 `C:` 盘一样操作。

### 常见 Provider 类型

| Provider    | 示例驱动器       | 说明             |
| :---------- | :--------------- | :--------------- |
| FileSystem  | `C:`, `D:`       | 本地文件系统     |
| Registry    | `HKLM:`, `HKCU:` | Windows 注册表   |
| Environment | `Env:`           | 环境变量         |
| Certificate | `Cert:`          | 证书存储         |
| Function    | `Function:`      | 当前会话中的函数 |
| Variable    | `Variable:`      | 当前定义的变量   |
| Alias       | `Alias:`         | 命令别名         |

### 示例：操作注册表

```
Get-ChildItem HKLM:\Software\Microsoft
```

就像浏览文件夹一样浏览注册表。