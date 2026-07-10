## labelstudio



### 启动参数



您可以使用命令行界面指定机器学习后端及其他选项。运行`label-studio --help`以查看所有可用选项，或参阅以下表格。

Label Studio 的一些可用命令可用于获取信息或启动 Label Studio 服务器：

| 命令                                                         | 描述                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| `label-studio`                                               | 启动 Label Studio 服务器。                                   |
| `label-studio -h` `label-studio --help`                      | 显示可用的命令行参数。                                       |
| `label-studio init <project_name> <optional_arguments>`      | 在 Label Studio 中初始化特定项目。                           |
| `label-studio start <project_name> --init <optional_arguments>` | 启动 Label Studio 服务器并初始化特定项目。                   |
| `label-studio reset_password`                                | 重置特定 Label Studio 用户的密码。请参阅[为 Label Studio 创建用户账户](https://labelstud.io/guide/signup). |
| `label-studio shell`                                         | 获取 Label Studio 的 Shell 访问权限，以直接操作数据。请参阅 Django shell-plus 命令的文档。 |
| `label-studio version`                                       | 显示 Label Studio 的版本号后退出。                           |
| `label-studio user --username <email>`                       | 显示带令牌的用户信息。                                       |



以下命令行参数为可选，必须在`label-studio start <argument> <value>`或作为环境变量，在您设置用于托管 Label Studio 的环境时指定：