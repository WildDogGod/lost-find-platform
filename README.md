# 校园失物招领平台

一个基于 Spring Boot 3 + Vue 3 的校园失物招领系统，支持寻物启事、招领启事发布，认领申请与审核，站内消息、收藏，以及管理员后台（用户管理、信息审核、数据统计）。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Spring Boot 3.5.6、JDK 17、MyBatis-Plus 3.5.8、JWT（jjwt 0.12.6）、阿里云 OSS V2 SDK（可选） |
| 数据库 | MySQL 8.x（库名 `lost_found`，utf8mb4） |
| 前端 | Vue 3.5、Vite 5、Element Plus 2.8、Pinia、Vue Router、Axios |

## 目录结构

```
lost-found-platform/
├── pom.xml                  父 POM（聚合 lost-found-common、lost-found-app）
├── lost-found-common/       公共模块：统一返回 Result、异常、常量、JWT 工具
├── lost-found-app/          业务模块：启动类、Controller、Service、Mapper、实体、配置
│   └── src/main/resources/  application.yaml / application-dev.yml
├── lost-found-ui/           前端工程（Vue3 + Vite）
└── sql/
    ├── schema.sql           建库建表（含分类基础数据）
    └── data.sql             示例数据（用户、物品、认领、消息、收藏）
```

## 环境要求

| 软件 | 版本 | 说明 |
|---|---|---|
| JDK | 17 | 必须 17，Spring Boot 3.5 不支持 8 |
| Maven | 3.8+ | 首次编译需联网下载依赖 |
| MySQL | 8.0+ | 字符集 utf8mb4 |
| Node.js | 18+ | 推荐 18 或 20 LTS |

## 快速开始（4 步）

### 第 1 步：初始化数据库

用 Navicat / MySQL 命令行依次执行：

```bash
mysql -uroot -p --default-character-set=utf8mb4 < sql/schema.sql
mysql -uroot -p --default-character-set=utf8mb4 lost_found < sql/data.sql
```

执行完成后应存在 6 张表：`user`、`category`、`item`、`claim`、`message`、`favorite`。

### 第 2 步：创建本地敏感配置文件（必做）

项目不会把数据库密码、JWT 密钥提交到代码里，需要在**用户目录**下新建：

- Windows：`C:\Users\你的用户名\.lost-found-platform\application-secret.yml`
- macOS / Linux：`~/.lost-found-platform/application-secret.yml`

内容如下（把值换成你自己的）：

```yaml
spring:
  datasource:
    username: root
    password: 你的MySQL密码

zzhx:
  alioss:
    # 没有阿里云 OSS 时，把 application-dev.yml 里的 enabled 改成 false，下面两行可删掉
    access-key-id: 你的AccessKeyId
    access-key-secret: 你的AccessKeySecret
  jwt:
    # 必须至少 32 个字符，随便换成一串随机字符串
    secret: 请替换为至少32位的随机字符串
    expiration-minutes: 1440
```

> 也可以用环境变量覆盖：`DB_USERNAME`、`DB_PASSWORD`、`ALIOSS_ACCESS_KEY_ID`、`ALIOSS_ACCESS_KEY_SECRET`、`JWT_SECRET`。
>
> ⚠️ 这个文件放在仓库外，**不要提交到 Git，也不要发给别人**。

### 第 3 步：启动后端

```bash
cd lost-found-platform
mvn clean install -DskipTests
mvn -pl lost-found-app spring-boot:run
```

看到 `Started LostFoundPlatformApplication` 即启动成功，服务地址 `http://localhost:8080`。

### 第 4 步：启动前端

```bash
cd lost-found-platform/lost-found-ui
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。前端已配置代理：`/api/**` 和 `/upload/**` 转发到 `localhost:8080`。

## 测试账号

导入 `sql/data.sql` 后可直接使用（密码均已实测验证）：

| 角色 | 账号 | 密码 | 说明 |
|---|---|---|---|
| 管理员 | `admin` | `admin123` | 登录后进入后台（用户管理 / 信息审核 / 数据统计） |
| 普通用户 | `zhangsan` | `123456` | 已实名认证，可直接发布/认领 |
| 普通用户 | `lisi` | `123456` | 已实名认证 |
| 普通用户 | `wangwu` | `123456` | 未实名认证（`verify_status=0`） |
| 普通用户 | `zhaoliu` | `123456` | 已实名认证 |

> 若本地数据库的 admin 密码被改过（例如曾重置为 `123456`），以实际库为准；也可以执行下面 SQL 重置为 `123456`：
>
> ```sql
> UPDATE `user`
> SET `password` = '$2a$10$ymi/5o3hNGtfGRh8yCngmuXGMaOX6GI.V1ulGdya1Dz6dXZyQdZBu'
> WHERE `username` = 'admin';
> ```

## 配置说明

### 文件上传（OSS 开关）

`lost-found-app/src/main/resources/application-dev.yml`：

```yaml
zzhx:
  alioss:
    enabled: false   # false = 存本地磁盘；true = 上传阿里云 OSS
    region: cn-beijing
    bucket-name: 你的bucket名
    dir: lost-found
```

- **推荐给别人演示时设为 `false`**：图片存到项目根目录 `upload/`，通过 `/upload/xxx` 访问，零外部依赖。
- 设为 `true` 时必须提供自己的 `access-key-id` / `access-key-secret`，且 bucket 地域要与 `region` 一致（V2 SDK 用 region 签名，不要填 endpoint）。

### 数据库连接

`application.yaml` 中默认连接 `localhost:3306/lost_found`。若数据库地址/端口不同，改这一行：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/lost_found?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&useSSL=false
```

## 常见问题

| 现象 | 原因与解决 |
|---|---|
| 启动报 `zzhx.jwt.secret 未配置或长度不足 32 字节` | 没建 `application-secret.yml`，或 secret 太短 |
| 启动报 `Port 8080 was already in use` | 8080 被占用：关掉旧进程，或改 `application.yaml` 的 `server.port` |
| 前端能打开但登录报错 / 列表空白 | 后端没启动，或后端启动失败；先确认 8080 有服务 |
| `mvn` 下载依赖很慢 | 在 Maven `settings.xml` 配置阿里云镜像 `https://maven.aliyun.com/repository/public` |
| 中文显示成 `????` | 用命令行执行 SQL 时加 `--default-character-set=utf8mb4` |
| 上传图片失败 | 检查 `zzhx.alioss.enabled`：没有 OSS 账号就设为 `false` |

## 主要接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/auth/register` | 注册 |
| POST | `/auth/login` | 登录，返回 JWT |
| POST | `/auth/logout` | 退出登录 |
| GET | `/items` | 物品列表（分页/筛选） |
| POST | `/items` | 发布寻物/招领 |
| GET | `/items/{id}` | 物品详情 |
| POST | `/claims` | 提交认领申请 |
| GET | `/messages` | 站内消息 |
| GET | `/admin/stats` | 后台数据统计 |
| PUT | `/admin/items/{id}/audit` | 信息审核 |

除登录/注册外，请求头需携带 `Authorization: Bearer <token>`。

统一返回格式：`{ "code": 200, "message": "success", "data": ... }`，`code=200` 成功，`1000` 业务失败，`401` 未登录。

## 构建打包（部署用）

```bash
# 后端可执行 jar
mvn clean package -DskipTests
# 产物：lost-found-app/target/lost-found-app-0.0.1-SNAPSHOT.jar
java -jar lost-found-app/target/lost-found-app-0.0.1-SNAPSHOT.jar

# 前端静态文件
cd lost-found-ui && npm run build
# 产物：lost-found-ui/dist/，可交给 Nginx 托管
```
