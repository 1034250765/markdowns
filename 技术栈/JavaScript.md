## 常见方法



`trim()` 是 JavaScript 字符串的**内置方法**，用于**移除字符串两端的空白字符**，并返回一个新的字符串。

`encodeURIComponent` 是 JavaScript 的**内置函数**，用于**对 URI（统一资源标识符）中的特定组件进行编码**，以便安全地放入 URL 中。

`Fetch API `是一种现代的、功能强大的网络请求工具，它允许你通过 JavaScript 异步地请求资源，而不需要使用传统的 XMLHttpRequest 对象。返回Response对象

```js
const res = fetch('https://api.example.com/data')
```

 `Response` 对象的关键属性和方法

- **`ok`**：布尔值，HTTP 状态码在 200–299 之间时为 `true`，否则 `false`。
- **`status`**：HTTP 状态码（如 200、404、500）。
- **`statusText`**：状态文本（如 "OK"、"Not Found"）。
- **`headers`**：`Headers` 对象，包含响应头信息。
- **`bodyUsed`**：布尔值，标记响应主体是否已被读取。

- **`res.json()`**：解析响应体为 JSON 对象（返回 Promise）。
- **`res.text()`**：返回纯文本字符串。
- **`res.blob()`**：返回二进制大对象（如图片、文件）。
- **`res.arrayBuffer()`**：返回 `ArrayBuffer`。
- **`res.formData()`**：解析为 `FormData` 对象。







## 解构赋值与语法糖

### 语法糖

**语法糖（syntactic sugar）**：不改变程序功能，只让代码更短、更好读的语法形式。它只是「写法上的便利」，区别于「不合法的投机写法」——它是语言规范的一部分，运行时会被还原成更基础的写法，这个还原过程叫**脱糖（desugaring）**。

```js
const x = obj.x      // 基础写法
const { x } = obj    // 语法糖，两者行为完全一致
```

常见的语法糖：

| 语法糖 | 脱糖后的基础写法 |
| --- | --- |
| `const { x } = obj` | `const x = obj.x` |
| `const [a, b] = arr` | `const a = arr[0]; const b = arr[1]` |
| 模板字符串 `` `${a}-${b}` `` | `a + '-' + b` |
| `(x) => x + 1` | `function (x) { return x + 1 }` |
| `for (const v of arr)` | 迭代器 + `while` |
| `a ?? b` | `a !== null && a !== undefined ? a : b` |
| `async` / `await` | Promise + `then` 链 |

判断标准很简单：**去掉糖，程序行为一模一样，只是变啰嗦。**

注意：语法糖 ≠ 性能优化。解构和 `obj.x` 在引擎里最终都是属性访问，两者没有性能差距，按可读性选就行。

### 解构赋值

**解构赋值（destructuring assignment）**：从对象中按**名字**、从数组中按**位置**取值，直接赋给变量。它本身就是一个语法糖。

#### 对象解构 —— 大括号，按名字

```js
const user = { name: '太阳', age: 20 }

const { name } = user      // name = '太阳'
```

左边的 `{ name }` **不是对象字面量**，而是一份取值清单：我要名为 `name` 的那个属性。它等价于 `const name = user.name`。

与直接访问的区别：

| 写法 | 结果 |
| --- | --- |
| `const a = user` | `a` 是**整个对象** |
| `const { a } = user` | `a` 是 `user.a` 的值 |

#### 常用变体

```js
const user = { name: '太阳', age: 20, addr: { city: '武汉' }, tags: [1, 2, 3] }

const { name, age } = user            // 一次拆多个
const { name: n } = user              // 改名：n = '太阳'（不再创建 name 变量）
const { age = 18 } = user             // 默认值：属性取不到时用 18
const { addr: { city } } = user       // 嵌套解构：city = '武汉'（addr 本身不会成为变量）
const { name, ...rest } = user        // 剩余：rest = { age, addr, tags }
const key = 'name'
const { [key]: v } = user             // 计算属性名：键名是变量时也能解构（写法偏绕）
```

**冒号方向**：`{ name: n }` 里的冒号不是赋值。左边 `name` 是源属性名，右边 `n` 是新变量名，方向和对象字面量**正好相反**（字面量是 `新名: 值`），容易记混。

#### 数组解构 —— 方括号，按位置

```js
const [first, second] = [10, 20]       // first = 10, second = 20
const [, , third] = [10, 20, 30]       // 用逗号跳过前两个，third = 30
const [head, ...tail] = [1, 2, 3]      // head = 1, tail = [2, 3]
```

数组没有属性名，所以按顺序取。一句话：**方括号按位置，大括号按名字。**

#### 函数参数解构

```js
function Card({ title, desc, onClose }) { ... }   // 签名即文档：一眼看出这个函数吃什么
function Card(props) { ... }                      // 得翻到函数体里才知道
```

#### 本文档里的实例

「方式二」那段的 `const { blob, filename } = await download(url)` 就是对象解构：`download` 返回 `{ blob, filename }`（见下方 `return { blob: ..., filename: ... }`），解构把这两个字段摊平成独立变量，后面 `triggerFileDownload(blob, filename)` 就能直接用。

当然也可以直接用对象：`const res = await download(url)`，再写 `res.blob` / `res.filename`。功能完全一样，只是多一层前缀。字段少、只取一两个时，直接访问反而更清楚。

#### 注意点

- **解构是一次性取值，不是拷贝**：`const { count } = state` 之后改 `state.count`，`count` 不会跟着变。要同步更新状态时必须留在对象上操作。
- **属性值是对象时仍是同一个引用**：`const { addr } = user` 拿到的 `addr` 和 `user.addr` 指向同一块内存，改里面的字段两边都会变。
- **不能解构 `null` / `undefined`**：`const { x } = null` 会直接抛 `TypeError`。接口数据可能为 null 时要兜底：`const { x } = res ?? {}`。
- **赋值解构必须加括号**：对已声明过的变量做解构赋值，`{ x } = obj` 会被解析成块语句而报错，要写成 `({ x } = obj)`。

#### 什么时候用哪个

- 字段成组、要往下传、函数参数 → **解构**，签名即文档
- 只用一两次、键名是动态变量（`obj[key]`）→ **直接访问**
- 需要保留整个对象、要展开合并 → 直接访问 + 对象展开 `{ ...obj, role: 'admin' }`

一句话总结：**解构是语法糖，不是必需品。它的价值不在少打字，而在把「我关心哪些字段」写显式。**



## fetch

```js
export async function getJson(path) {
  const res = await fetch(buildUrl(path))
  if (!res.ok) {
    throw new Error(await extractError(res))
  }
  return res.json()
}
```

fetch 的返回值类型是 Promise<Response>。

- 这里 res 的类型就是 Response

- await res.json() 返回解析后的 JSON（通常是对象/数组，取决于后端）
- await res.text() 返回字符串
- await res.blob() 返回二进制 Blob



```python
                return FileResponse(
                    archive_path,
                    media_type="application/zip",
                    filename=download_name,
                    headers=_attachment_headers(download_name),
                )
    #后端返回 file response
```

> window.location.assign(getDatasetDirectDownloadUrl(datasetId))

浏览器直接跳转下载（最简单）

优点：代码简单、浏览器原生下载。
缺点：拿不到响应体，无法做细粒度错误处理和自定义逻辑。



方式二：fetch 拿 Blob 再触发下载（可控）
适合需要统一错误处理、按钮 loading、前端二次处理文件名。

```js
const { blob, filename } = await download(url)
triggerFileDownload(blob, filename)
```

对应流程是：

1. fetch 请求后端 FileResponse 接口。
2. res.blob() 读取文件二进制。
3. 从响应头解析文件名（你已在 [client.js:75](vscode-file://vscode-app/d:/yingyong/Microsoft VS Code/8b640eef5a/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 做了）。
4. 用 a 标签 + URL.createObjectURL 触发保存（你已在 [client.js:54](vscode-file://vscode-app/d:/yingyong/Microsoft VS Code/8b640eef5a/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 做了）。

```js
export async function download(path, options = {}) {
  const res = await fetch(buildUrl(path), options)
  if (!res.ok) {
    throw new Error(await extractError(res))
  }
  return {
    blob: await res.blob(),
    filename: getFilenameFromResponse(res.headers) || inferFilenameFromContentType(res.headers),
  }
}


export function triggerFileDownload(blob, filename) {
  const url = URL.createObjectURL(blob)   #这行代码的意思是：把内存里的二进制文件对象 blob 临时变成一个“可访问的本地                                             #URL 字符串”。
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

const a = document.createElement('a')
创建一个临时的 a 标签（下载链接）。

a.href = url
把链接指向前面生成的 blob 地址（内存文件地址）。

a.download = filename
告诉浏览器“下载时用这个文件名保存”，而不是直接打开页面。

document.body.appendChild(a)
把这个临时链接插入页面，保证后面的 click 在各浏览器都可触发。

a.click()
程序触发一次点击，浏览器开始下载。

a.remove()
下载动作触发后，马上把临时 a 标签从 DOM 删除，避免页面残留无用节点。

setTimeout(() => URL.revokeObjectURL(url), 1000)
1 秒后释放 blob URL 对应的内存，避免内存泄漏。
之所以不是立刻释放，是给浏览器一点时间完成下载触发。

```

