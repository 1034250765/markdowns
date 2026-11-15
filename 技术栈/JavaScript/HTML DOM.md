
## HTML DOM (文档对象模型)

当网页被加载时，浏览器会创建页面的文档对象模型（Document Object Model）。

**HTML DOM** 模型被构造为**对象**的树：

![替代文字](https://www.runoob.com/images/pic_htmltree.gif)


在 JavaScript 中，document.write() 可用于直接向 HTML 输出流写内容。

```TS
<!DOCTYPE html><html>
<body>
<script>
document.write(Date());
</script>
</body>
</html>
```

修改 HTML 内容的最简单的方法是使用 innerHTML 属性。

如需改变 HTML 元素的内容，请使用这个语法：

```TS

document.getElementById(_id_).innerHTML=_新的 HTML_
```


如需改变 HTML 元素的属性，请使用这个语法：

```ts
document.getElementById(_id_)._attribute=新属性值_


<!DOCTYPE html><html>
<body>
<img id="image" src="smiley.gif">
<script>
document.getElementById("image").src="landscape.jpg";
</script>
</body>
</html>
```

**`addEventListener()` 用来监听事件，并指定事件发生时要执行的函数。** 例如，点击按钮、输入文字、按下键盘时，都可以执行相应的代码。

```ts
<button id="btn">点我</button>

<script>
  const button = document.getElementById("btn");

  function handleClick(event) {
    button.textContent = "你点击了按钮！";
    console.log(event.target);
  }

  button.addEventListener("click", handleClick);
</script>
```

**`button.onclick = 函数`**，它和 `addEventListener()` 都能让按钮在被点击时执行代码。**主要区别是：`onclick` 只有一个处理函数的位置，而 `addEventListener()` 可以注册多个不同的处理函数。**

## 创建新的 HTML 元素 (节点) - appendChild()

```ts
<div id="div1">
<p id="p1">这是一个段落。</p>
<p id="p2">这是另外一个段落。</p>
</div>
 
<script>
var para = document.createElement("p");
var node = document.createTextNode("这是一个新的段落。");
para.appendChild(node);
 
var element = document.getElementById("div1");
element.appendChild(para);
</script>
```

## 浏览器对象模型 (BOM)

## Window 对象

所有浏览器都支持 window 对象。它表示浏览器窗口。

所有 JavaScript 全局对象、函数以及变量均自动成为 window 对象的成员。

全局变量是 window 对象的属性。

全局函数是 window 对象的方法。

甚至 HTML DOM 的 document 也是 window 对象的属性之一

window.screen 对象包含有关用户屏幕的信息。

window.location 对象用于获得当前页面的地址 (URL)，并把浏览器重定向到新的页面。

window.history 对象包含浏览器的历史。

window.navigator 对象包含有关访问者浏览器的信息。

Cookie 用于存储 web 页面的用户信息。

## JavaScript 框架（库）

JavaScript 高级程序设计（特别是对浏览器差异的复杂处理），通常很困难也很耗时。

为了应对这些调整，许多的 **JavaScript (helper)** 库应运而生。

这些 JavaScript 库常被称为 **JavaScript 框架**。

在本教程中，我们将了解到一些广受欢迎的 JavaScript 框架：

- jQuery
- Prototype
- MooTools

所有这些框架都提供针对常见 JavaScript 任务的函数，包括动画、DOM 操作以及 Ajax 处理。

在本教程中，您将学习到如何开始使用它们，来使得 JavaScript 编程更容易、更安全且更有乐趣。

