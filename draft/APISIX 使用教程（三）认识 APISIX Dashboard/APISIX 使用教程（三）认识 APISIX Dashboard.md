## HTTP 接口准备

使用 Spring Boot Web 快速暴露一个 http 接口，接口地址为：http://宿主机IP:8188/index，接口响应返回响应时间和请求头信息。

controller 源码

```java
package cn.woodwhales.apisixdemo;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * @author woodwhales on 2025-05-25 21:12
 */
@Slf4j
@RequestMapping
@RestController
public class IndexController {

    @GetMapping("index")
    public Object index(@RequestHeader Map<String, String> headers) {
        Map<String, Object> result = new HashMap<>();
        result.put("time", System.currentTimeMillis());
        result.put("header", headers);
        return result;
    }
}
```

application.yml 配置
```yml
server:
  port: 8188
  address: 0.0.0.0
```

使用浏览器直接访问服务接口，请求响应为：

```json
{
    "host": "172.21.250.70:8188",
    "connection": "keep-alive",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,zh-TW;q=0.5"
}
```

## 基础路由配置

希望达到如下功能：

![](images/01.png)

**步骤1**：创建路由

![](images/02.png)

**步骤2**：配置路由

- 路由名称：自由填写，保证唯一即可
- 路径：`/apisix-demo/*`
- 路径改写：选择正则改写
- 匹配正则表达式：`^/apisix-demo/(.*)`
- 转发路径模板：`/$1`

其他全部默认，点击下一步

![](images/03.png)

**步骤3**：设置上游服务

- 选择上游服务：手动填写
- 目标节点：填写业务系统的 IP 和端口号
- 协议：默认为 HTTP，保持不变即可

其他全部默认，点击下一步

![](images/04.png)

**步骤4**：插件配置

不启动任何插件，直接点击下一步

**步骤5**：预览

检查路由配置是否正确，如果有问题则点击上一步重新配置，否则点击提交。

上述路由创建成功之后，在路由列表中可见，点击：更多里面的查看，可以看到路由的完整配置：

![](images/05.png)

从路由详情配置可以看出，该路由使用了`proxy-rewrite`插件。

此时浏览器请求：http://APISIX系统的IP:9080/apisix-demo/index，响应数据是业务系统的 /index 接口响应。

## 上游服务配置

上节是最基础的路由配置，如果需要更多的路由指向相同的上游服务，则可以统一配置一个上游服务，与之相关的路由配置关联这个上游服务配置即可。

**步骤1**：创建上游服务

![](images/06.png)

**步骤2**：创建上游服务

![](images/07.png)

**步骤3**：预览上游服务配置

如果配置没有问题，则直接点击提交。

配置好上游服务后，可以在路由配置中直接选择这个上游服务配置，不再需要手动配置：

![](images/08.png)

此时查看路由配置详情，可以看到上游服务配置是上游服务配置 ID：

![](images/09.png)

## 消费者配置

**步骤1**：在消费者列表中创建消费者

![](images/10.png)

**步骤2**：填写消费者名称

![](images/11.png)

**步骤3**：插件配置

可以对消费者配置插件，想要开启插件，则点击启动并配置对应插件参数即可。不想启用任何插件直接点击下一步即可：

![](images/12.png)

这里开启了`key-auth`插件

![](images/13.png)

**步骤3**：预览

检查所有配置是否无误，没有则点击提交。

**步骤4**：查看消费者配置详情

![](images/14.png)

注意，只对消费者配置了`key-auth`插件不能对任何路由生效，需要在要限制的路由配置中开启相应插件才能生效。

即应该先增加路由插件，所有用户访问该路由时，会匹配对应消费者插件配置。

![](images/15.png)

此时浏览器访问：http://APISIX系统的IP:9080/apisix-demo/index时，响应不成功，响应状态码为`401`

```json
{"message":"Missing API key in request"}
```

在请求头中携带`apiKey`信息，如果匹配不正确也不会响应成功，响应状态码为`401`

```json
{"message":"Invalid API key in request"}
```

## jwt-auth 插件使用

### HS256 算法认证

在消费者配置 jwt-auth 插件开启，并设置插件参数：

```json
{
  "username": "user1",
  "plugins": {
    "jwt-auth": {
      "_meta": {
        "disable": false
      },
      "algorithm": "HS256",
      "exp": 86400,
      "key": "user1",
      "secret": "mySecretKey1234567890abcdefghijklmnopqr"
    }
  }
}
```

maven 项目引入依赖：

```xml
<dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.12.6</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.12.6</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>0.12.6</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.8.25</version>
        </dependency>
```

gradle 项目引入依赖：

```groovy
implementation 'io.jsonwebtoken:jjwt-api:0.12.6'
runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.12.6'
runtimeOnly 'io.jsonwebtoken:jjwt-jackson:0.12.6'
implementation 'cn.hutool:hutool-all:5.8.25'
```

java 生成 jwt token 示例：

```
import cn.hutool.core.date.DateUtil;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

import java.security.Key;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * @author woodwhales on 2025-05-26 0:05
 */
public class JwtTokenTool {

    public static String genToken() {
        // secret 至少32字符
        String secret = "mySecretKey1234567890abcdefghijklmnopqr";
        Key key = Keys.hmacShaKeyFor(secret.getBytes());

        // 2. 设置JWT Claims
        Map<String, Object> claims = new HashMap<>();
        claims.put("key", "user1");

        Date now = new Date();

        // 3. 生成Token（有效期1天）
        String jwtToken = Jwts.builder()
                .claims(claims)
                // 签发时间
                .setIssuedAt(now)
                // 过期时间
                .expiration(DateUtil.offsetDay(now, 1))
                // 使用HS256算法和密钥
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
        return jwtToken;
    }
}
```

在请求头中携带 key 为：`authorization`，value 是：`Bearer` + "空格" + {JWT Token}

### RS256 算法认证

消费者插件配置，注意：

`public_key`必须含有：`-----BEGIN PUBLIC KEY-----`和`-----END PUBLIC KEY-----`，密钥的信息是要求以`\n`拼接。

`private_key`必须含有：`-----BEGIN PRIVATE KEY-----`和`-----END PRIVATE KEY-----`，密钥的信息是要求以`\n`拼接。

```json
{
  "username": "user1",
  "plugins": {
    "jwt-auth": {
      "_meta": {
        "disable": false
      },
      "algorithm": "RS256",
      "exp": 86400,
      "key": "user1",
      "private_key": "-----BEGIN PRIVATE KEY-----\nM...AN\n-----END PRIVATE KEY-----",
      "public_key": "-----BEGIN PUBLIC KEY-----\nM...==\n-----END PUBLIC KEY-----"
    }
  }
}
```

#### 使用 openssl 生成 RSA 密钥对

**步骤1**：生成 4096 位 RSA 私钥

```shell
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:4096
```

**步骤2**：提取公钥

```shell 
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

**步骤3**：将私钥换行符替换为：\n

```shell
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' private_key.pem | sed 's/\\n$//' > private_key_single_line.txt
```

**步骤4**：将公钥换行符替换为：\n


```shell
awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' public_key.pem | sed 's/\\n$//' > public_key_single_line.txt
```

#### 使用 java 生成 RSA 密钥对

```java
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import java.security.KeyPair;
import java.security.PrivateKey;
import java.security.PublicKey;

public class RsaKeyGenerator {
    
    public static void genKeyPair() {
        // 生成 RSA 密钥对（2048位）
        KeyPair keyPair = Keys.keyPairFor(SignatureAlgorithm.RS256);
        
        PrivateKey privateKey = keyPair.getPrivate(); // 用于签名
        PublicKey publicKey = keyPair.getPublic();    // 用于验证

        System.out.println("Private Key (Base64):\n" + 
            java.util.Base64.getEncoder().encodeToString(privateKey.getEncoded()));
        System.out.println("\nPublic Key (Base64):\n" + 
            java.util.Base64.getEncoder().encodeToString(publicKey.getEncoded()));
    }
}
```

java 生成 jwt token

```java
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import java.security.PrivateKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class JwtRsaGenerator {
    public static void main(String[] args) {
        // 1. 从文件或配置加载私钥（此处直接使用生成的私钥）
        String privateKeyBase64 = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7..."; 
        PrivateKey privateKey = Keys.hmacShaKeyFor(
            java.util.Base64.getDecoder().decode(privateKeyBase64)
        );

        // 2. 设置 JWT Claims
        Map<String, Object> claims = new HashMap<>();
        claims.put("userId", 123);
        claims.put("role", "admin");

        // 3. 生成 Token（有效期1小时）
        String jwtToken = Jwts.builder()
                .setClaims(claims)
                .setSubject("user-auth")
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + 3600 * 1000))
                 // 使用 RSA 私钥签名    
                .signWith(privateKey, SignatureAlgorithm.RS256) 
                .compact();

        System.out.println("Generated JWT Token (RS256):\n" + jwtToken);
    }
}
```

