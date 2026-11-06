## JavaScript 输出

JavaScript 没有任何打印或者输出的函数。
JavaScript 可以通过不同的方式来输出数据：
- 使用 **window.alert()** 弹出警告框。
- 使用 **document.write()** 方法将内容写到 HTML 文档中。
- 使用 **innerHTML** 写入到 HTML 元素。
- 使用 **console.log()** 写入到浏览器的控制台。


## 操作 HTML 元素

如需从 JavaScript 访问某个 HTML 元素，您可以使用 document.getElementById(_id_) 方法。

## 写到 HTML 文档

出于测试目的，您可以将JavaScript直接写在HTML 文档中：

```ts
<!DOCTYPE html><html>
<body><h1>我的第一个 Web 页面</h1>
	<p>我的第一个段落。</p>
	<script>document.write(Date());
</script>

</body>
</html>
```


## JavaScript 语法

JavaScript 是一个脚本语言。

它是一个轻量级，但功能强大的编程语言。

## JavaScript 字面量

在编程语言中，一般固定值称为字面量，如 3.14。

**数字（Number）字面量** 可以是整数或者是小数，或者是科学计数(e)。

**字符串（String）字面量** 可以使用单引号或双引号:

```ts
"John Doe"
'John Doe'
```

**表达式字面量** 用于计算：

```ts
5 + 6
5 * 10
```

**数组（Array）字面量** 定义一个数组：

```ts
[40, 100, 1, 5, 25, 10]
```

**对象（Object）字面量** 定义一个对象：

```ts
{firstName:"John", lastName:"Doe", age:50, eyeColor:"blue"}
```
**函数（Function）字面量** 定义一个函数：

```ts
function myFunction(a, b) { return a * b;}
```

## JavaScript 变量

在编程语言中，变量用于存储数据值。

JavaScript 使用关键字 **var** 来定义变量， 使用等号来为变量赋值：

```ts
var x, length
x = 5
length = 6
```

JavaScript使用 **算术运算符** 来计算值:
JavaScript使用**赋值运算符**给变量赋值：
在 HTML 中，JavaScript 语句用于向浏览器发出命令。

语句是用分号分隔：

```ts
x = 5;  
y = 6;  
z = (x + y) * 10;
```

## JavaScript 注释

不是所有的 JavaScript 语句都是"命令"。双斜杠 **//** 后的内容将会被浏览器忽略：

```ts

// 我不会执行
```

## JavaScript 数据类型

JavaScript 有多种数据类型：数字，字符串，数组，对象等等：

```ts
var length = 16;                                  // Number 通过数字字面量赋值 
var points = x * 10;                              // Number 通过表达式字面量赋值
var lastName = "Johnson";                         // String 通过字符串字面量赋值
var cars = ["Saab", "Volvo", "BMW"];              // Array  通过数组字面量赋值
var person = {firstName:"John", lastName:"Doe"};  // Object 通过对象字面量赋值
```

## JavaScript 变量

变量是用于存储信息的"容器"。

在 JavaScript 中，变量用于存储数据，并可以在程序执行过程中动态更改。

在 JavaScript 中，变量可以存储各种类型的数据，如数字、字符串、对象、函数等。

变量名是标识符，用于引用存储在变量中的数据。

在 JavaScript 中，可以使用 var、let 和 const 关键字来声明变量。


- **`var`**：ES5 引入的变量声明方式，具有函数作用域。
    
- **`let`**：ES6 引入的变量声明方式，具有块级作用域。
    
- **`const`**：ES6 引入的常量声明方式，具有块级作用域，且值不可变。

您可以在一条语句中声明很多变量。该语句以 var 开头，并使用逗号分隔变量即可：

```ts
var lastname="Doe", age=30, job="carpenter";
```

在计算机程序中，经常会声明无值的变量。未使用值来声明的变量，其值实际上是 undefined。

在执行过以下语句后，变量 carname 的值将是 undefined：

```ts
var carname;
```

## JavaScript 数据类型

---

**值类型(基本类型)**：字符串（String）、数字(Number)、布尔(Boolean)、空（Null）、未定义（Undefined）、Symbol。

**引用数据类型（对象类型）**：对象(Object)、数组(Array)、函数(Function)，还有两个特殊的对象：正则（RegExp）和日期（Date）。

## JavaScript 拥有动态类型

JavaScript 拥有动态类型。这意味着相同的变量可用作不同的类型：

```ts
var x;               
	// x 为 undefinedvar x = 5;           
	// 现在 x 为数字
var x = "John";      // 现在 x 为字符串
```

变量的数据类型可以使用 typeof 操作符来查看：

```ts
typeof "John"                // 返回 string
typeof 3.14                  // 返回 number
typeof false                 // 返回 boolean
typeof [1,2,3,4]             // 返回 object
typeof {name:'John', age:34} // 返回 object
```

## JavaScript 对象

对象由花括号分隔。在括号内部，对象的属性以名称和值对的形式 (name : value) 来定义。属性由逗号分隔：

```ts

var person={firstname:"John", lastname:"Doe", id:5566};
```


当您声明新变量时，可以使用关键词 "new" 来声明其类型：

```ts
var carname=new String;  
var x=      new Number;  
var y=      new Boolean;  
var cars=   new Array;  
var person= new Object;
```

在 JavaScript中，几乎所有的事物都是对象。

可以说 "JavaScript 对象是变量的容器"。

但是，我们通常认为 "JavaScript 对象是键值对的容器"。

键值对通常写法为 **name : value** (键与值以冒号分割)。

键值对在 JavaScript 对象通常称为 **对象属性**。

你可以通过两种方式访问对象属性:

```ts
person.lastName;

person["lastName"];
```

对象的方法定义了一个函数，并作为对象的属性存储。

对象方法通过添加 () 调用 (作为一个函数)。

```ts
name = person.fullName();


```

你可以使用以下语法创建对象方法：

```ts
methodName : function() {
    // 代码 }
```

## JavaScript 函数
函数是由事件驱动的或者当它被调用时执行的可重复使用的代码块。

```ts
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>测试实例</title>
<script>
function myFunction()
{
    alert("Hello World!");
}
</script>
</head>
 
<body>
<button onclick="myFunction()">点我</button>
</body>
</html>
```


如果您把值赋给尚未声明的变量，该变量将被自动作为 window 的一个属性。

这条语句：  carname="Volvo";

将声明 window 的一个属性 carname。

非严格模式下给未声明变量赋值创建的全局变量，是全局对象的可配置属性，可以删除。

## JavaScript 作用域

作用域是可访问变量的集合。

在 JavaScript 中, 对象和函数同样也是变量。

**在 JavaScript 中, 作用域为可访问变量，对象，函数的集合。**

JavaScript 函数作用域: 作用域在函数内修改。

变量在函数内声明，变量为局部变量，具有局部作用域。

局部变量：只能在函数内部访问。

变量在函数外定义，即为全局变量。

全局变量有 **全局作用域**: 网页中所有脚本和函数均可使用。

如果变量在函数内没有声明（没有使用 var 关键字），该变量为全局变量。

以下实例中 carName 在函数内，但是为全局变量。

```ts
// 此处可调用 carName 变量
 
function myFunction() {
    carName = "Volvo";
    // 此处可调用 carName 变量
}
```

在 HTML 中, 全局变量是 window 对象，所以 window 对象可以调用函数内的未声明（未加 var)的局部变量。

## JavaScript 事件

HTML 事件是发生在 HTML 元素上的事情。

当在 HTML 页面中使用 JavaScript 时， JavaScript 可以触发这些事件。

HTML 事件可以是浏览器行为，也可以是用户行为。

以下是 HTML 事件的实例：

- HTML 页面完成加载
- HTML input 字段改变时
- HTML 按钮被点击

通常，当事件发生时，你可以做些事情。

在事件触发时 JavaScript 可以执行一些代码。

HTML 元素中可以添加事件属性，使用 JavaScript 代码来添加 HTML 元素。

```ts

<some-HTML-element some-event='JavaScript 代码'>

<some-HTML-element some-event="JavaScript 代码">


```

## 常见的HTML事件

下面是一些常见的HTML事件的列表:

| 事件          | 描述                    |
| ----------- | --------------------- |
| onchange    | HTML 元素改变             |
| onclick     | 用户点击 HTML 元素          |
| onmouseover | 鼠标指针移动到指定的元素上时发生      |
| onmouseout  | 用户从一个 HTML 元素上移开鼠标时发生 |
| onkeydown   | 用户按下键盘按键              |
| onload      | 浏览器已完成页面的加载           |

## JavaScript 字符串

---

JavaScript 字符串用于存储和处理文本。

字符串可以存储一系列字符，如 "John Doe"。

字符串可以是插入到引号中的任何字符。你可以使用单引号或双引号

你可以使用索引位置来访问字符串中的每个字符

可以使用内置属性 **length** 来计算字符串的长度

通常， JavaScript 字符串是原始值，可以使用字符创建： **var firstName = "John"**

但我们也可以使用 new 关键字将字符串定义为一个对象： **var firstName = new String("John")**

## 字符串属性

|属性|描述|
|---|---|
|constructor|返回创建字符串属性的函数|
|length|返回字符串的长度|
|prototype|允许您向对象添加属性和方法|

  

---

## 字符串方法

更多方法实例可以参见：[JavaScript String 对象](https://www.runoob.com/jsref/jsref-obj-string.html)。

|方法|描述|
|---|---|
|charAt()|返回指定索引位置的字符|
|charCodeAt()|返回指定索引位置字符的 Unicode 值|
|concat()|连接两个或多个字符串，返回连接后的字符串|
|fromCharCode()|将 Unicode 转换为字符串|
|indexOf()|返回字符串中检索指定字符第一次出现的位置|
|lastIndexOf()|返回字符串中检索指定字符最后一次出现的位置|
|localeCompare()|用本地特定的顺序来比较两个字符串|
|match()|找到一个或多个正则表达式的匹配|
|replace()|替换与正则表达式匹配的子串|
|search()|检索与正则表达式相匹配的值|
|slice()|提取字符串的片断，并在新的字符串中返回被提取的部分|
|split()|把字符串分割为子字符串数组|
|substr()|从起始索引号提取字符串中指定数目的字符|
|substring()|提取字符串中两个指定的索引号之间的字符|
|toLocaleLowerCase()|根据主机的语言环境把字符串转换为小写，只有几种语言（如土耳其语）具有地方特有的大小写映射|
|toLocaleUpperCase()|根据主机的语言环境把字符串转换为大写，只有几种语言（如土耳其语）具有地方特有的大小写映射|
|toLowerCase()|把字符串转换为小写|
|toString()|返回字符串对象值|
|toUpperCase()|把字符串转换为大写|
|trim()|移除字符串首尾空白|
|valueOf()|返回某个字符串对象的原始值|
# JavaScript 模板字符串

JavaScript 中的模板字符串是一种方便的字符串语法，允许你在字符串中嵌入表达式和变量。

模板字符串使用反引号 `` 作为字符串的定界符分隔的字面量。

模板字面量是用反引号（`）分隔的字面量，允许多行字符串、带嵌入表达式的字符串插值和一种叫带标签的模板的特殊结构。
`string text ${expression} string text`


## JavaScript 错误 - throw、try 和 catch

**try** 语句测试代码块的错误。

**catch** 语句处理错误。

**throw** 语句创建自定义错误。

**finally** 语句在 try 和 catch 语句之后，无论是否有触发异常，该语句都会执行。

```ts
try {
    ...    //异常的抛出
} catch(e) {
    ...    //异常的捕获与处理
} finally {
    ...    //结束处理
}
```

## Throw 语句

throw 语句允许我们创建自定义错误。

正确的技术术语是：创建或**抛出异常**（exception）。

如果把 throw 与 try 和 catch 一起使用，那么您能够控制程序流，并生成自定义的错误消息。

```ts
function myFunction() {
    var message, x;
    message = document.getElementById("message");
    message.innerHTML = "";
    x = document.getElementById("demo").value;
    try { 
        if(x == "")  throw "值为空";
        if(isNaN(x)) throw "不是数字";
        x = Number(x);
        if(x < 5)    throw "太小";
        if(x > 10)   new ValidationError("邮箱格式不正确", "email");
    }
    catch(err) {
        message.innerHTML = "错误: " + err;
    }
}
```


## JavaScript 声明提升

JavaScript 中，函数及变量的声明都将被提升到函数的最顶部。

JavaScript 中，变量可以在使用后声明，也就是变量可以先使用再声明。

以下两个实例将获得相同的结果

## JavaScript 初始化不会提升

JavaScript 初始化不会提升，JavaScript 只有声明的变量部分会提升，初始化部分不会。

## JavaScript this 关键字

面向对象语言中 this 表示当前对象的一个引用。

但在 JavaScript 中 this 不是固定不变的，它会随着执行环境的改变而改变。

- 在方法中，this 表示该方法所属的对象。
- 如果单独使用，this 表示全局对象。
- 在函数中，this 表示全局对象。
- 在函数中，在严格模式下，this 是未定义的(undefined)。
- 在事件中，this 表示接收事件的元素。

## JavaScript 函数定义

---

JavaScript 使用关键字 **function** 定义函数。

函数可以通过声明定义，也可以是一个表达式。

```ts
function myFunction(a, b) {  
    return a * b;  
}
```

JavaScript 函数可以通过一个表达式定义。

函数表达式可以存储在变量中：

```ts
var x = function (a, b) {return a * b};
```

在 JavaScript 中使用 **typeof** 操作符判断函数类型将返回 "function" 。

但是JavaScript 函数描述为一个对象更加准确。

JavaScript 函数有 **属性** 和 **方法**。

arguments.length 属性返回函数调用过程接收到的参数个数：

toString() 方法将函数作为一个字符串返回:

ES6 新增了箭头函数。

箭头函数表达式的语法比普通函数表达式更简洁。

```ts
(参数1, 参数2, …, 参数N) => { 函数声明 }

(参数1, 参数2, …, 参数N) => 表达式(单一)

(x, y) => { return x * y };
```

## 默认参数

ES5 中如果函数在调用时未提供隐式参数，参数会默认设置为： **undefined**

有时这是可以接受的，但是建议最好为参数设置一个默认值：

```ts
function myFunction(x, y = 10) { // y is 10 if not passed or undefined return x + y; }
```

JavaScript 函数有个内置的对象 arguments 对象。

arguments 对象包含了函数调用的参数数组。

通过这种方式你可以很方便的找到最大的一个参数的值：

```ts
x = sumAll(1, 123, 500, 115, 44, 88); function sumAll() { var i, sum = 0; for (i = 0; i < arguments.length; i++) { sum += arguments[i]; } return sum; }
```

在 JavaScript 中你可以将函数定义为对象的方法。

以下实例创建了一个对象 (**myObject**), 对象有两个属性 (**firstName** 和 **lastName**), 及一个方法 (**fullName**):

```ts
var myObject = {
    firstName:"John",
    lastName: "Doe",
    fullName: function () {
        return this.firstName + " " + this.lastName;
    }
}
myObject.fullName();         // 返回 "John Doe"
```

如果函数调用前使用了 **new** 关键字, 则是调用了构造函数。

这看起来就像创建了新的函数，但实际上 JavaScript 函数是重新创建的对象：

```ts
// 构造函数:
function myFunction(arg1, arg2) {
    this.firstName = arg1;
    this.lastName  = arg2;
}
 
// This    creates a new object
var x = new myFunction("John","Doe");
x.firstName;                             // 返回 "John"
```

## 作为函数方法调用函数

在 JavaScript 中, 函数是对象。JavaScript 函数有它的属性和方法。

**call()** 和 **apply()** 是预定义的函数方法。 两个方法可用于调用函数，两个方法的第一个参数必须是对象本身。

```ts
function myFunction(a, b) {
    return a * b;
}
myObject = myFunction.call(myObject, 10, 2);     // 返回 20\

function myFunction(a, b) {
    return a * b;
}
myArray = [10, 2];
myObject = myFunction.apply(myObject, myArray);  // 返回 20


```

## JavaScript 闭包

---

JavaScript 变量可以是局部变量或全局变量。

私有变量可以用到闭包。

函数可以访问函数外部定义的变量，如：

var a = 4; function myFunction() { return a * a; }

```ts
function add() { 
var counter = 0;
 function plus() { 
 counter += 1; 
 return counter; }
  return plus; // 将内部函数返回出去 }
```

## JavaScript 类(class)

**类是用于创建对象的模板。**

我们使用 class 关键字来创建一个类，类体在一对大括号 {} 中，我们可以在大括号 {} 中定义类成员的位置，如方法或构造函数。

每个类中包含了一个特殊的方法 constructor()，它是类的构造函数，这种方法用于创建和初始化一个由 **class** 创建的对象。

```ts
class ClassName { constructor() { ... } }
```

```ts
class Runoob {
  constructor(name, url) {
    this.name = name;
    this.url = url;
  }
}
```

定义好类后，我们就可以使用 new 关键字来创建对象：

```ts

class Runoob {
  constructor(name, url) {
    this.name = name;
    this.url = url;
  }
}
 
let site = new Runoob("菜鸟教程",  "https://www.runoob.com");****
```


