
## Node.js 基础概念

Node.js 是一个基于 Chrome V8 JavaScript 引擎构建的 JavaScript 运行时环境。简单来说，Node.js 让 JavaScript 可以在服务器端运行，而不仅仅局限于浏览器中。

nvm（Node Version Manager）是一个非常有用的工具，可以让您在同一台机器上安装和管理多个 Node.js 版本。


**为什么需要 nvm？**

- 不同项目可能需要不同版本的 Node.js
- 测试应用在不同 Node.js 版本下的兼容性
- 方便升级和降级 Node.js 版本

## 创建 Node.js 应用

### 步骤一、使用 require 指令来加载和引入模块

语法格式如下：

```ts
const module = require('module-name');
```

其中，module-name 可以是一个文件路径（相对或绝对路径），也可以是一个模块名称，如果是一个模块名称，Node.js 会自动从 node_modules 目录中查找该模块。

require 指令会返回被加载的模块的导出对象，可以通过该对象来访问模块中定义的属性和方法，如果模块中有多个导出对象，则可以使用解构赋值的方式来获取它们。

我们使用 **require** 指令来载入 http 模块，并将实例化的 HTTP 赋值给变量 http，实例如下:

```ts
var http = require("http");
```


### 步骤二、创建服务器

接下来我们使用 http.createServer() 方法创建服务器，并使用 listen 方法绑定 8888 端口。 函数通过 request, response 参数来接收和响应数据。

实例如下，在你项目的根目录下创建一个叫 server.js 的文件，并写入以下代码：

```ts
var http = require('http');

http.createServer(function (request, response) {

        // 发送 HTTP 头部 
        // HTTP 状态值: 200 : OK
        // 内容类型: text/plain
        response.writeHead(200, {'Content-Type': 'text/plain'});

        // 发送响应数据 "Hello World"
        response.end('Hello World\n');
}).listen(8888);

// 终端打印如下信息
console.log('Server running at http://127.0.0.1:8888/');
```

## Node.js 工作机制

Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行时环境，它让开发者能够使用 JavaScript 编写服务器端代码。与传统的服务器端技术不同，Node.js 采用了**事件驱动**和**非阻塞 I/O**模型，这使得它特别适合处理高并发的网络应用。

### 核心特点

1. **单线程**：Node.js 使用单线程处理请求
2. **事件循环**：通过事件驱动机制处理并发
3. **非阻塞 I/O**：I/O 操作不会阻塞主线程
4. **跨平台**：可以在 Windows、Linux、macOS 等系统上运行

## Promise

Promise 是 ES6 引入的异步编程解决方案，它表示一个异步操作的最终完成或失败及其结果值。

```ts
const fs = require('fs').promises;

// 使用 Promise 读取文件
fs.readFile('example.txt', 'utf8')
  .then(data => {
    console.log('文件内容:', data);
  })
  .catch(err => {
    console.error('读取文件出错:', err);
  });

console.log('读取文件请求已发送，继续执行其他代码...');
```

## Node.js 事件循环


事件循环是 Node.js 处理非阻塞 I/O 操作的核心机制，使得单线程能够高效处理多个并发请求。

Node.js 是基于单线程的 JavaScript 运行时，利用事件循环来处理异步操作，如文件读取、网络请求和数据库查询。

事件循环使得 Node.js 能够非阻塞地运行代码、处理多个连接、以及执行异步 I/O 操作。

事件循环使得 Node.js 能够处理大量并发的 I/O 操作而不会导致线程阻塞，这是 Node.js 高效处理并发请求的关键。

默认情况下，你的 JavaScript 代码主要在一个主线程上执行。但底层的异步操作可以借助操作系统或线程池进行。例如，`fs.readFile()` 的文件读取工作由底层线程池处理，完成后，再由事件循环安排执行你的 JS 回调。**后台操作可以同时进行，不代表这些 JS 回调也在同时执行。**

## 导入内置模块

内置模块是由 Node.js 自带的模块，在安装 Node.js 时就已经包含在环境中，因此无需额外安装。常见的内置模块包括 fs、http、path、os、crypto 等。

导入内置模块只需要使用 require() 函数并传入模块名称即可。

```ts
// 导入文件系统模块
const fs = require('fs');

// 导入路径模块
const path = require('path');

// 导入 HTTP 模块
const http = require('http');
```

第三方模块是开发者或开源社区发布的模块，可以通过 npm（Node 包管理器）安装到项目中，常见的第三方模块有 express、lodash、axios 等。

第三方模块安装后，这些模块会被放置在项目的 node_modules 目录下。要导入一个第三方模块，同样使用 require() 函数，但传入的是模块的名称。

## 自定义模块导出与导入（CommonJS 模块）

**1、导出模块：**使用 module.exports 或 exports 将函数、对象或变量导出。

**2、导入模块：**使用 require() 导入模块。

在 Node.js 中，引入一个模块非常简单，如下我们创建一个 **main.js** 文件并引入 hello 模块，代码如下:

### 导入模块

在 Node.js 中，引入一个模块非常简单，如下我们创建一个 **main.js** 文件并引入 hello 模块，代码如下:

```ts
var hello = require('./hello');
hello.world();
```

接下来我们就来创建 hello.js 文件，代码如下：

```ts
exports.world = function() {
    console.log('Hello World');
}
```

ES 模块使用 import 和 export，是现代 JavaScript 的模块规范。

- ES 模块使用 `import` 和 `export` 关键字，需将文件扩展名设置为 `.mjs`，或者在 `package.json` 中声明 `"type": "module"`。
- ES 模块支持静态导入（`import ... from ...`）和动态导入（`import()`）。
```ts
// myModule.mjs
export function greet(name) {
  return `Hello, ${name}!`;
}

// main.mjs
import { greet } from './myModule.mjs';
console.log(greet('Bob')); // 输出：Hello, Bob!
```

## ES Module（ESM）规范

ESM 是 JavaScript 官方的模块标准，它采用异步加载，并且是浏览器和现代 Node.js 应用的首选。

在 ESM 中，你使用 import 语句来导入模块，使用 export 语句来导出模块。

**启用 ESM：**要在 Node.js 中使用 ESM，你需要在 package.json 文件中添加 "type": "module"，或者将文件扩展名更改为 .mjs。

**导出模块:**

```ts
// math.mjs
export function add(a, b) {
  return a + b;
}

export default function multiply(a, b) {
  return a * b;
}
```

```ts
// app.mjs  
import multiply, { add } from './math.mjs';  
  
console.log(add(2, 3));      // 5  
console.log(multiply(2, 3)); // 6
```

