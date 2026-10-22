
## 第一个 Go 程序

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```
运行方式有两种：直接执行（不产生二进制文件）或编译后执行。

```cmd
# 方式一：直接运行（开发调试时常用）
$ go run main.go
Hello, RUNOOB!
欢迎来到 Go 语言的世界

# 方式二：编译为二进制文件后执行（生产部署时常用）
$ go build -o hello main.go
$ ./hello
Hello, RUNOOB!
欢迎来到 Go 语言的世界
```

## Go 语言用途

Go 语言被设计成一门应用于搭载 Web 服务器，存储集群或类似用途的巨型中央服务器的系统编程语言。

对于高性能分布式系统领域而言，Go 语言无疑比大多数其它语言有着更高的开发效率。它提供了海量并行的支持，这对于游戏服务端的开发而言是再好不过了。

### 静态类型与类型推断

Go 是**静态类型**语言，所有变量类型在编译时即确定。但与 C/Java 不同的是，Go 支持类型**推断**——编译器可以自动推导变量类型，开发者无需反复声明类型名。

这种设计在保持类型安全的同时，让代码写起来像动态语言一样简洁。

```go
package main

import "fmt"

func main() {
    // 完整声明：显式指定类型
    var name string = "runoob"

    // 类型推断：编译器自动推导类型
    var version = 1.24      // 推导为 float64
    count := 100            // 短变量声明，推导为 int
    message := "Hello Go"   // 推导为 string

    // 多变量声明
    x, y := 10, 20          // 同时声明多个变量

    fmt.Println(name, version, count, message, x, y)
}
```

### 丰富的标准库

Go 的标准库覆盖了现代开发的大部分需求，无需引入第三方依赖即可完成常见任务。下表列出了最常用的标准库包：

| 包名            | 功能           | 典型用途                       |
| ------------- | ------------ | -------------------------- |
| net/http      | HTTP 客户端与服务端 | 构建 Web 服务、RESTful API      |
| encoding/json | JSON 编解码     | API 数据序列化与反序列化             |
| database/sql  | 数据库访问接口      | 配合驱动操作 MySQL、PostgreSQL 等  |
| os            | 操作系统交互       | 文件读写、环境变量、进程管理             |
| fmt           | 格式化输入输出      | 打印日志、格式化字符串                |
| sync          | 同步原语         | Mutex、WaitGroup、Once 等并发控制 |
| testing       | 测试框架         | 单元测试、基准测试、示例测试             |
| time          | 时间处理         | 计时器、定时器、时间格式化              |
| context       | 上下文传递        | 超时控制、请求取消、值传递              |
| io            | I/O 抽象       | 统一的读写接口                    |
| crypto        | 加密算法         | 哈希、对称/非对称加密、TLS            |
| flag          | 命令行参数解析      | CLI 工具开发                   |

## Go语言结构
Go 语言的基础组成有以下几个部分：

- 包声明
- 引入包
- 函数
- 变量
- 语句 & 表达式
- 注释

package main
_package main_ 定义了包名。你必须在源文件中非注释的第一行指明这个文件属于哪个包，如：package main。package main表示一个可独立执行的程序，每个 Go 应用程序都包含一个名为 main 的包。

_import "fmt"_ 告诉 Go 编译器这个程序需要使用 fmt 包（的函数，或其他元素），fmt 包实现了格式化 IO（输入/输出）的函数。

_func main()_ 是程序开始执行的函数。main 函数是每一个可执行程序所必须包含的，一般来说都是在启动后第一个执行的函数

 /*...*/ 是注释，单行注释是最常见的注释形式，你可以在任何地方使用以 // 开头的单行注释。

_fmt.Println(...)_ 可以将字符串输出到控制台，并在最后自动增加换行字符 \n。  
使用 fmt.Print("hello, world\n") 可以得到相同的结果。

当标识符（包括常量、变量、类型、函数名、结构字段等等）以一个大写字母开头，如：Group1，那么使用这种形式的标识符的对象就可以被外部包的代码所使用（客户端程序需要先导入这个包），这被称为导出（像面向对象语言中的 public）；标识符如果以小写字母开头，则对包外是不可见的。


需要注意的是 { 不能单独放在一行，所以以下代码在运行时会产生错误：

```go
package main

import "fmt"

func main()  
{  // 错误，{ 不能在单独的行上
    fmt.Println("Hello, World!")
}
```


Go 语言中使用 fmt.Sprintf 或 fmt.Printf 格式化字符串并赋值给新串

```go
package main

import (
    "fmt"
)

func main() {
   // %d 表示整型数字，%s 表示字符串
    var stockcode=123
    var enddate="2020-12-31"
    var url="Code=%d&endDate=%s"
    var target_url=fmt.Sprintf(url,stockcode,enddate)
    fmt.Println(target_url)
}
//Code=123&endDate=2020-12-31
```

## Go 语言数据类型

|序号|类型和描述|
|---|---|
|1|**布尔型**  <br>布尔型的值只可以是常量 true 或者 false。一个简单的例子：var b bool = true。|
|2|**数字类型**  <br>整型 int 和浮点型 float32、float64，Go 语言支持整型和浮点型数字，并且支持复数，其中位的运算采用补码。|
|3|**字符串类型:**  <br>字符串就是一串固定长度的字符连接起来的字符序列。Go 的字符串是由单个字节连接起来的。Go 语言的字符串的字节使用 UTF-8 编码标识 Unicode 文本。|
|4|**派生类型:**  <br>包括：<br><br>- (a) 指针类型（Pointer）<br>- (b) 数组类型<br>- (c) 结构化类型(struct)<br>- (d) Channel 类型<br>- (e) 函数类型<br>- (f) 切片类型<br>- (g) 接口类型（interface）<br>- (h) Map 类型|

## Go 语言变量

Go 语言变量名由字母、数字、下划线组成，其中首个字符不能为数字。

声明变量的一般形式是使用 var 关键字：

**var identifier type**

可以一次声明多个变量：

**var identifier1, identifier2 type**

// 声明一个变量并初始化  ,**根据值自行判定变量类型。**
    **var a = "RUNOOB"**

intVal := 1 相等于： 只能函数内部使用

```go
var intVal int 
intVal =1 
```

```go

//类型相同多个变量, 非全局变量
var vname1, vname2, vname3 type
vname1, vname2, vname3 = v1, v2, v3

var vname1, vname2, vname3 = v1, v2, v3 // 和 python 很像,不需要显示声明类型，自动推断

vname1, vname2, vname3 := v1, v2, v3 // 出现在 := 左侧的变量不应该是已经被声明过的，否则会导致编译错误

// 这种因式分解关键字的写法一般用于声明全局变量
var (
    vname1 v_type1
    vname2 v_type2
)
```


###  值类型和引用类型

当使用等号 `=` 将一个变量的值赋值给另一个变量时，如：`j = i`，实际上是在内存中将 i 的值进行了拷贝：

![[Pasted image 20261018184259.png]]

你可以通过 &i 来获取变量 i 的内存地址，例如：0xf840000040（每次的地址都可能不一样）。值类型变量通常存储在栈中，尤其是当它们是局部变量时。当值类型变量的值需要在函数作用域之外使用时，Go 会将其分配到堆内存中。

内存地址会根据机器的不同而有所不同，甚至相同的程序在不同的机器上执行后也会有不同的内存地址。因为每台机器可能有不同的存储器布局，并且位置分配也可能不同。

更复杂的数据通常会需要使用多个字，这些数据一般使用引用类型保存。

一个引用类型的变量 r1 存储的是 r1 的值所在的内存地址（数字），或内存地址中第一个字所在的位置。

![[Pasted image 20261018184657.png]]


这个内存地址称之为指针，这个指针实际上也被存在另外的某一个值中。

同一个引用类型的指针指向的多个字可以是在连续的内存地址中（内存布局是连续的），这也是计算效率最高的一种存储形式；也可以将这些字分散存放在内存中，每个字都指示了下一个字所在的内存地址。

## Go 语言常量

常量是一个简单值的标识符，在程序运行时，不会被修改的量。常量中的数据类型只可以是布尔型、数字型（整数型、浮点型和复数）和字符串型。

**单词释义**： `const` 是 `constant`（常量）的缩写，表示程序中不可变的值。

常量的定义格式：

```go
const identifier [type] = value
```


### iota 常量计数器

`iota` 是 Go 语言的特殊常量，也称为常量计数器。它可以在 const 声明块中自动生成递增的序列值。

**重要特性**：

- `iota` 在 `const` 关键字出现时将被重置为 0。
- const 中每新增一行常量声明，iota 自动计数加 1。
- 可以理解为 const 语句块中的行索引（从 0 开始）。
```go

package main

  

import "fmt"

  

// iota 从 0 开始，每行加 1

const (

    a = iota   // 0

    b          // 1（省略值，默认使用上一行的 iota）

    c          // 2

)

  

func main() {

    fmt.Printf("a=%d, b=%d, c=%d\n", a, b, c)

    fmt.Printf("iota = %d", iota)

}
```



- 当常量值省略时，默认使用上一行的 iota 值。
- 因此 b=1, c=2。


下表列出了Go语言的其他运算符。

|运算符|描述|实例|
|---|---|---|
|&|返回变量存储地址|&a; 将给出变量的实际地址。|
|*|指针变量。|*a; 是一个指针变量|

## Go 语言函数


Go 语言函数定义格式如下：

```go
func function_name( [parameter list] ) [return_types] {
   函数体
}
```

函数定义解析：

- func：函数由 func 开始声明
- function_name：函数名称，参数列表和返回值类型构成了函数签名。
- parameter list：参数列表，参数就像一个占位符，当函数被调用时，你可以将值传递给参数，这个值被称为实际参数。参数列表指定的是参数类型、顺序、及参数个数。参数是可选的，也就是说函数也可以不包含参数。
- return_types：返回类型，函数返回一列值。return_types 是该列值的数据类型。有些功能不需要返回值，这种情况下 return_types 不是必须的。
- 函数体：函数定义的代码集合。

以下实例为 max() 函数的代码，该函数传入两个整型参数 num1 和 num2，并返回这两个参数的最大值：

```go

/* 函数返回两个数的最大值 */
func max(num1, num2 int) int {
   /* 声明局部变量 */
   var result int

   if (num1 > num2) {
      result = num1
   } else {
      result = num2
   }
   return result 
}
```

Go 函数可以返回多个值，例如：

```go
package main

import "fmt"

func swap(x, y string) (string, string) {
   return y, x
}

func main() {
   a, b := swap("Google", "Runoob")
   fmt.Println(a, b)
}
```

### Go 语言函数引用传递值

引用传递是指在调用函数时将实际参数的地址传递到函数中，那么在函数中对参数所进行的修改，将影响到实际参数。

引用传递指针参数传递到函数内，以下是交换函数 swap() 使用了引用传递：

```go
/* 定义交换值函数*/
func swap(x *int, y *int) {
   var temp int
   temp = *x    /* 保持 x 地址上的值 */
   *x = *y      /* 将 y 值赋给 x */
   *y = temp    /* 将 temp 值赋给 y */
}
```

### Go 语言函数作为实参

Go 语言中，函数是一等公民（First-class citizen），可以像普通变量一样被赋值、传递和使用。将函数作为实参传递给另一个函数，是 Go 中常见的编程模式，常用于回调、策略模式等场景。

函数可以赋值给一个变量，通过该变量来调用函数：

```go
package main

import (
    "fmt"
    "math"
)

func main() {
    /* 将匿名函数赋值给变量 getSquareRoot */
    getSquareRoot := func(x float64) float64 {
        return math.Sqrt(x)
    }

    /* 通过变量调用函数 */
    fmt.Println(getSquareRoot(9))   // 输出：3
    fmt.Println(getSquareRoot(16))  // 输出：4
}
```

将函数作为实参传递给另一个函数时，接收方需要声明对应的函数类型参数。以下示例定义了一个 `apply` 函数，接收一个操作函数和两个操作数，对两个数执行任意指定的操作：

```go
package main

import (
    "fmt"
    "math"
)

/* 定义一个函数，接收一个函数类型的参数 op */
/* op 的类型为 func(float64, float64) float64，表示接受两个 float64 参数、返回 float64 的函数 */
func apply(op func(float64, float64) float64, a, b float64) float64 {
    return op(a, b)
}

func main() {
    /* 定义加法函数 */
    add := func(a, b float64) float64 {
        return a + b
    }

    /* 定义乘法函数 */
    multiply := func(a, b float64) float64 {
        return a * b
    }

    /* 将 add 函数作为实参传入 apply */
    fmt.Println(apply(add, 3, 4))       // 输出：7

    /* 将 multiply 函数作为实参传入 apply */
    fmt.Println(apply(multiply, 3, 4))  // 输出：12

    /* 也可以直接传入匿名函数 */
    fmt.Println(apply(func(a, b float64) float64 {
        return math.Pow(a, b) // a 的 b 次方
    }, 2, 10))                          // 输出：1024
}
```
### Go 语言函数闭包（匿名函数）
Go 语言支持匿名函数，可作为闭包。匿名函数是一个"内联"语句或表达式。匿名函数的优越性在于可以直接使用函数内的变量，不必申明。匿名函数是一种没有函数名的函数，通常用于在函数内部定义函数，或者作为函数参数进行传递。

```go
package main

import "fmt"

func getSequence() func() int {
   i:=0
   return func() int {
      i+=1
     return i  
   }
}

func main(){
   /* nextNumber 为一个函数，函数 i 为 0 */
   nextNumber := getSequence()  

   /* 调用 nextNumber 函数，i 变量自增 1 并返回 */
   fmt.Println(nextNumber())
   fmt.Println(nextNumber())
   fmt.Println(nextNumber())
   
   /* 创建新的函数 nextNumber1，并查看结果 */
   nextNumber1 := getSequence()  
   fmt.Println(nextNumber1())
   fmt.Println(nextNumber1())
}
```

## Go 语言变量作用域

在函数体内声明的变量称之为局部变量，它们的作用域只在函数体内，参数和返回值变量也是局部变量。

以下实例中 main() 函数使用了局部变量 a, b, c：

```go
package main

import "fmt"

func main() {
   /* 声明局部变量 */
   var a, b, c int 

   /* 初始化参数 */
   a = 10
   b = 20
   c = a + b

   fmt.Printf ("结果： a = %d, b = %d and c = %d\n", a, b, c)
}
```

在函数体外声明的变量称之为全局变量，全局变量可以在整个包甚至外部包（被导出后）使用。

全局变量可以在任何函数中使用，以下实例演示了如何使用全局变量：

```go
package main

import "fmt"

/* 声明全局变量 */
var g int

func main() {

   /* 声明局部变量 */
   var a, b int

   /* 初始化参数 */
   a = 10
   b = 20
   g = a + b

   fmt.Printf("结果： a = %d, b = %d and g = %d\n", a, b, g)
}
```

形式参数会作为函数的局部变量来使用。实例如下：

```go

package main

import "fmt"

/* 声明全局变量 */
var a int = 20;

func main() {
   /* main 函数中声明局部变量 */
   var a int = 10
   var b int = 20
   var c int = 0

   fmt.Printf("main()函数中 a = %d\n",  a);
   c = sum( a, b);
   fmt.Printf("main()函数中 c = %d\n",  c);
}

/* 函数定义-两数相加 */
func sum(a, b int) int {
   fmt.Printf("sum() 函数中 a = %d\n",  a);
   fmt.Printf("sum() 函数中 b = %d\n",  b);

   return a + b;
}
```

不同类型的局部和全局变量默认值为：

| 数据类型    | 初始化默认值 |
| ------- | ------ |
| int     | 0      |
| float32 | 0      |
| pointer | nil    |

## Go 语言数组

Go 语言提供了数组类型的数据结构。

数组是具有相同唯一类型的一组已编号且长度固定的数据项序列，这种类型可以是任意的原始类型例如整型、字符串或者自定义类型。

相对于去声明 **number0, number1, ..., number99** 的变量，使用数组形式 **numbers[0], numbers[1] ..., numbers[99]** 更加方便且易于扩展。

数组元素可以通过索引（位置）来读取（或者修改），索引从 0 开始，第一个元素索引为 0，第二个索引为 1，以此类推。

![[Pasted image 20261021132557.png]]

Go 语言数组声明需要指定元素类型及元素个数，语法格式如下：

```go
var arrayName [size]dataType
```
以下演示了数组初始化：

以下实例声明一个名为 numbers 的整数数组，其大小为 5，在声明时，数组中的每个元素都会根据其数据类型进行默认初始化，对于整数类型，初始值为 0。

```go
var numbers = [5]int{1, 2, 3, 4, 5}
```

在 Go 语言中，数组的大小是类型的一部分，因此不同大小的数组是不兼容的，也就是说 [5]int 和 [10]int 是不同的类型。

如果数组长度不确定，可以使用 ... 代替数组的长度，编译器会根据元素个数自行推断数组的长度：

```go
var balance = [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
或
balance := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
```

如果设置了数组的长度，我们还可以通过指定下标来初始化元素：

```go
//  将索引为 1 和 3 的元素初始化
balance := [5]float32{1:2.0,3:7.0}
```

数组元素可以通过索引（位置）来读取。格式为数组名后加中括号，中括号中为索引的值。

## Go 语言指针

Go 语言中指针是很容易学习的，Go 语言中使用指针可以更简单的执行一些任务。

接下来让我们来一步步学习 Go 语言指针。

我们都知道，变量是一种使用方便的占位符，用于引用计算机内存地址。

Go 语言的取地址符是 &，放到一个变量前使用就会返回相应变量的内存地址。

以下实例演示了变量在内存中地址：

```go
package main

import "fmt"

func main() {
   var a int = 10   

   fmt.Printf("变量的地址: %x\n", &a  )
}
```

一个指针变量指向了一个值的内存地址。

类似于变量和常量，在使用指针前你需要声明指针。指针声明格式如下：

```go
var var_name *var-type
```

在指针类型前面加上 * 号（前缀）来获取指针所指向的内容。

```go
package main

import "fmt"

func main() {
   var a int= 20   /* 声明实际变量 */
   var ip *int        /* 声明指针变量 */

   ip = &a  /* 指针变量的存储地址 */

   fmt.Printf("a 变量的地址是: %x\n", &a  )

   /* 指针变量的存储地址 */
   fmt.Printf("ip 变量储存的指针地址: %x\n", ip )

   /* 使用指针访问值 */
   fmt.Printf("*ip 变量的值: %d\n", *ip )
}
```

当一个指针被定义后没有分配到任何变量时，它的值为 nil。

nil 指针也称为空指针。

nil在概念上和其它语言的null、None、nil、NULL一样，都指代零值或空值。

一个指针变量通常缩写为 ptr。

## Go 语言结构体
Go 语言中数组可以存储同一类型的数据，但在结构体中我们可以为不同项定义不同的数据类型。

结构体是由一系列具有相同类型或不同类型的数据构成的数据集合。

结构体表示一项记录，比如保存图书馆的书籍记录，每本书有以下属性：

- Title ：标题
- Author ： 作者
- Subject：学科
- ID：书籍ID
结构体定义需要使用 type 和 struct 语句。struct 语句定义一个新的数据类型，结构体中有一个或多个成员。type 语句设定了结构体的名称。结构体的格式如下：

```go
type struct_variable_type struct {
   member definition
   member definition
   ...
   member definition
}
```

一旦定义了结构体类型，它就能用于变量的声明，语法格式如下：

```go
package main

import "fmt"

type Books struct {
   title string
   author string
   subject string
   book_id int
}


func main() {

    // 创建一个新的结构体
    fmt.Println(Books{"Go 语言", "www.runoob.com", "Go 语言教程", 6495407})

    // 也可以使用 key => value 格式
    fmt.Println(Books{title: "Go 语言", author: "www.runoob.com", subject: "Go 语言教程", book_id: 6495407})

    // 忽略的字段为 0 或 空
   fmt.Println(Books{title: "Go 语言", author: "www.runoob.com"})
}
```

如果要访问结构体成员，需要使用点号 . 操作符，格式为：
结构体.成员名