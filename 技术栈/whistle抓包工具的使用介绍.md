---
title: "whistle抓包工具的使用介绍"
source: "https://juejin.cn/post/7057334893973340174"
author:
  - "[[YX先生]]"
published: 2022-01-26
created: 2026-11-12
description: "一：简介 1：常用的抓包软件比较 1:mac的Charles 2:windows的filddler 有平台限制，配置较繁琐。 2：whistle的优势 免费，开源，跨平台的代理抓包软件。配置相对简单，"
tags:
  - "clippings"
---
## 一：简介

## 1：常用的抓包软件比较

1:mac的Charles

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fb18e452880f4576a8400cbf7792055b~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

2:windows的filddler

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e6cea8c3231a4cacb10ac1b2c9ce054b~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

有平台限制，配置较繁琐。

## 2：whistle的优势

免费，开源，跨平台的代理抓包软件。配置相对简单，功能强大，可以通过node模块扩展功能

官网： [wproxy.org/whistle/](https://link.juejin.cn/?target=https%3A%2F%2Fwproxy.org%2Fwhistle%2F "https://wproxy.org/whistle/")

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a4066c7475d24ee8b3f74f6f00d0ec41~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

gitHub: [github.com/avwo/whistl…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Favwo%2Fwhistle "https://github.com/avwo/whistle")

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e4cde0e41fff4ca78d5e0e916f78f5fd~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

主要的功能简介

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/00281a2a7cd5415ab012d164d3a4435a~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/841094f509fc4cfebfa2b8f88b257c89~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 二：安装和启动

## 1：安装node

```arduino
代码解读复制代码https://nodejs.org （官网下载对应的node,一般推荐长期稳定版本 LTS）
需要node的版本是大于  v0.10.0
查看自己本地node  版本号 node -v
```

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d1e5fb35295542d1a22a9d0998bf67dc~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/040de2e1eb354b05b0886ef5331f74c2~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 2: 安装 whistle

```
代码解读复制代码npm  i -g whistle
```

## 3: 启动

1）w2 start

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/767e733b3b434f20807d814369f6de61~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

默认端口为8899，若有冲突或者被占用，可以使用 w2 start -p 新的端口号 重置端口

浏览器访问， [http://127.0.0.1:8899/](https://link.juejin.cn/?target=http%3A%2F%2F127.0.0.1%3A8899%2F "http://127.0.0.1:8899/") 出现如下界面说明启动成功

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5dacec5ab77e43ba85e94c6b46b7e4fe~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 4：常用命令

w2 或者 whistle help 查看帮助信息

w2 restart 重启（改了userList.json文件中数据之后要重启才生效的）

w2 stop 关闭

## 三：谷歌浏览器安装插件

安装启动whistle后，通常浏览器需要设置代理指向whistle Server地址127.0.0.1:8899，为了方便切换，chrome下推荐安装使用proxyOmega插件来提高切换效率，这样就可以一键切换代理

下载地址：

[github.com/FelisCatus/…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FFelisCatus%2FSwitchyOmega%2Freleases "https://github.com/FelisCatus/SwitchyOmega/releases")

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/da8c6cf1d2da48b1b47a3c08414ab8e4~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

在谷歌的扩展程序中拖入

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a9d03911cca74e4cb5b06b4a4db3aed8~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4bb55a4a103948f9aa70ff628871f1d3~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

界面效果为

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d8f4bba186df4609ab42aeff84c0c5cb~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 四：功能和使用

## 1：监听抓包指定的域名下的请求

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/cdf93994279c4542b2e268d936f7750c~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

效果图

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2b0a395058de4fa7b0c510b23903f863~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/52f7037f8bbe4dafbe7cd33961ae0ff5~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 2：资源请求转发（将线上资源文件替换为本地的文件）

如果线上环境有特殊问题。没法在生产环境复现，这个时候就可以直接替换js文件到本地进行调试，提高调试效率。

1. ### 替换线上的js为本地js（可以排查线上的js文件版本不对啊，内容有错之类）

prepend 表示在前面加，body 表示直接替换，append 表示在后面加

eg: 将百度首页加载的jquery文件替换为自己本地指定的文件

[dss0.bdstatic.com/5aV1bjqh\_Q2…](https://link.juejin.cn/?target=https%3A%2F%2Fdss0.bdstatic.com%2F5aV1bjqh_Q23odCf%2Fstatic%2Fsuperman%2Fjs%2Flib%2Fjquery-1-edb203c114.10.2.js "https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/js/lib/jquery-1-edb203c114.10.2.js") file:///Users/Yelei/Desktop/share/baidu\_insert.js

在value中的配置（两种方式有差异）

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/dfe8730fde7141da8d30876dc951da1e~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

1）使用绝对路径的引用方式

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e18fecf8073a4f3592be03fe0eebfaef~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2999ebb442a343b385d49bf1aa35f2c8~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

2） 使用引入value中引入的内容。此方式保留了原文件

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/df99d65d9ce74902864dd4ac49cd658e~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

[dss0.bdstatic.com/5aV1bjqh\_Q2…](https://link.juejin.cn/?target=https%3A%2F%2Fdss0.bdstatic.com%2F5aV1bjqh_Q23odCf%2Fstatic%2Fsuperman%2Fjs%2Flib%2Fjquery-1-edb203c114.10.2.js "https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/js/lib/jquery-1-edb203c114.10.2.js") jsPrepend://{baidu\_insert.js}

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e6f3b4e3dadd463f84bfa3ee60d2756b~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

1. 替换为另一线上路径

比如访问随便一个网址，可以将其指向到想对应域名去

[123.com](https://link.juejin.cn/?target=http%3A%2F%2F123.com "http://123.com") [www.baidu.com](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com "https://www.baidu.com")

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7fccfc3674b047e19b34d7c349d85935~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 3: 注入html, css，js

注入的文件内容可以是保存在自己电脑中的文件，也可以写在value中。两种方式都可以

1. ### css注入，改变百度首页的字体颜色为红色

存储在自己电脑上

[www.baidu.com](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com "https://www.baidu.com") css:///Users/Yelei/Desktop/share/baidu\_resect.css

存储values中的

[www.baidu.com](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com "https://www.baidu.com") cssPrepend://{baidu\_resect.css}

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fbc531f6dd854146bcb971dfb95be115~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

存储在files文件中的

[www.baidu.com](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com "https://www.baidu.com") css:///$whistle/baidu\_resect.css

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/bed585b9bcd94e219234456fd1908c05~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

存储在files中的文件

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8030a666f2c142f7a4d502931d994e89~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

效果：

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a752cd9ffab2491aa540e445999da52b~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?) 1: js注入，百度首页注入vconsole.js

方式一：下载源码到本地

将vconsole.js的源码和初始化代码放在values中，在替换即可

[www.baidu.com](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com "https://www.baidu.com") jsPrepend://{vConsole.min.js} #引入源码

[www.baidu.com](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com "https://www.baidu.com") jsPrepend://{vconsole.js} #引入实例化的js

方式二：使用whistle提供的插件

npm i whistle.inspect

[www.baidu.com](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com%2F "https://www.baidu.com/") whistle.inspect://

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/0168f13898e04ee79803006c93a15ec9~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

2.html的注入

在百度首页增加一个宽高为100的红色盒子

[www.baidu.com](https://link.juejin.cn/?target=http%3A%2F%2Fwww.baidu.com "http://www.baidu.com") htmlPrepend://{addDom.html}

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d2ef13069c4e4d339ba89da058b58d4e~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 4：访问自己的数据，模拟mock

[http://api/users/getUsers](https://link.juejin.cn/?target=http%3A%2F%2Fapi%2Fusers%2FgetUsers "http://api/users/getUsers") file:///Users/Yelei/Desktop/share/users.json

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d78c71c6960444ab9b1b11c658c0cbbf~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

## 5: 手机代理到whistle

手机上安装https的证书

安装证书的步骤 参考文章： [cloud.tencent.com/developer/a…](https://link.juejin.cn/?target=https%3A%2F%2Fcloud.tencent.com%2Fdeveloper%2Farticle%2F1861183 "https://cloud.tencent.com/developer/article/1861183")

ios的在pc上下载之后（通过扫描pc端的https的二维码弹框下载证书），

或者通过微信/qq，把pc端的下载好了之后的证书文件在传递过去。

安装完成证书之后就可以在pc上使用界面了监听抓包在手机的应用。

设置 => 已下载描述文件 = >

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4045cc8f433249b78f94fbf1dced6d59~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7f6466d0bb8f4e6cb476f59bd9afaddc~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/25defae77afc438d9bdaf44391447f25~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/45743a6977d04499925c907339dd744f~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

将电脑、手机连在同一个局域网下 (一般连同一个 wifi 就可以，公司有网络策略限制得再想办法)，点击 whistle 界面右上角的 Online，配置自己手机的代理地址为online中的ip地址即可，就能在桌面端监测抓包手机上的应用

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d1b588d7b4849bc8b251b37edeb078a~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)