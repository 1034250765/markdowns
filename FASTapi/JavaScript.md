## 常用方法

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

