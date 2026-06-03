## Vite 是什么？

Vite 是一款由尤雨溪（Vue.js 作者）开发的构建工具，专为现代前端项目而设计。

Vite 的配置文件 `vite.config.js` 是 Vite 项目中的核心配置文件。通过这个文件，你可以对项目的开发服务器、插件系统、打包配置等进行自定义。

```js
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  // 配置选项
});

```

## Vite 配置结构

Vite 的配置文件包含多个配置项，常见的配置项包括 `root`、`base`、`server`、`build` 和 `plugins`。接下来我们将逐一介绍每个配置项的作用及其常见用法。

#### root - 项目根目录

```js
export default defineConfig({
  root: './src', // 将根目录设置为 src 文件夹
});
```

##### port - 指定端口-server - 开发服务器配置

```js
export default defineConfig({
  server: {
    port: 8080, // 修改开发服务器端口为 8080
  },
});
```

##### proxy - 代理配置-server - 开发服务器配置

如果你的项目需要与后端 API 进行通信，可以通过 `proxy` 配置项为开发服务器配置代理，以避免跨域问题。

```js
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 代理到后端 API 服务
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // 去除 /api 前缀
      },
    },
  },
});

```

##### 使用插件

```js
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()], // 使用 Vue 插件
});

```



## 前后端交互

```js
const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000/api'
```

- **`import.meta.env`**
  Vite 提供的**环境变量对象**，可以读取 `.env` 文件中定义的变量。
- **`VITE_API_BASE`**
  一个**自定义环境变量名**。
  Vite 规定只有以 `VITE_` 开头的变量才会暴露给客户端代码。你可以在项目根目录的 `.env` 或 `.env.development` 文件中设置它

- **`??`**（空值合并运算符）
  如果左侧的值为 `null` 或 `undefined`，则取右侧的默认值；否则取左侧的值。
  注意：空字符串 `""` 或 `0` 不会触发默认值，这与 `||` 不同。

**HTTP默认请求头**

```js
const defaultHeaders = {
  'Content-Type': 'application/json',
}
```

**`fetch`** 是 JavaScript 内置的**用于发起网络请求的 Web API**（浏览器环境），也存在于 Node.js 的实验性版本或通过 `node-fetch` 等库支持。

```js
const res = await fetch(buildUrl(path))
```

