## JS 基础

浏览器有三大解释器：

- HTML 解释器
- JavaScript 解释器
- CSS 解释器

浏览器5个组件：

- 用户界面
- 浏览器引擎
- 渲染引擎
- 数据存储
- 网络

## JS 进阶

事件循环

原型链

异步编程

浏览器存储

跨域

webpack 打包

## chrome 开发者工具奇技淫巧

### Network 面板

1. 在 network 面板中，可以按`shift`键位，鼠标移动到指定 URL 中，可以查看下方依赖的所有资源。也可以点击依赖的 URL 查看是源自哪个 URL。

2. 在 network 面板的过滤选项中，可以按`ctrl`键位，进行多选。

3. 在 network 面板的过滤选项中，搜索框中可以写一些过滤语法

4. 右击某个URL，选择：`Copy` →`Copy as cURL (bash)`，打开 postman，选择`File` →`Import...`，粘贴 cURL 文本，选择指定的`Collection name`。导入后，在右侧快捷选项中选择`Code`，可以在下拉选中选择 python 代码或者 Java 代码等。

### Sources 面板

选择`Overrides`，点击`Select folder for overrrides`，选择一个空文件夹，此时浏览器会提示"DevTools 请求获得对 xxx 的完整访问权限。"字样，点击`允许`按钮。勾选`Enable Local Overrides`。在`Network`中选择要保存的 URL，右击选择：`Orverride Content`，将该 URL 保存到这个指定空文件夹中。此时修改本地的页面 html 源码，再次刷新页面，此时页面的页面渲染也会变动。