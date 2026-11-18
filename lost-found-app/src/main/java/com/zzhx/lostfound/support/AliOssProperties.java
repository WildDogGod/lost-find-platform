package com.zzhx.lostfound.support;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * 阿里云 OSS 配置项（application-dev.yml 中的 zzhx.alioss.*）。
 */
@Component
@ConfigurationProperties(prefix = "zzhx.alioss")
@Data
public class AliOssProperties {

    /**
     * 上传开关：true 使用 OSS，false 退回本地磁盘。
     * 该值同时被 OssConfiguration 的 @ConditionalOnProperty 读取，决定是否创建 AliOssUtil。
     */
    private boolean enabled = true;

    private String region;
    private String accessKeyId;
    private String accessKeySecret;
    private String bucketName;

    /**
     * 文件存放在 bucket 下的目录前缀，例如 lost-found；
     * 最终对象名为 {@code lost-found/2026/10/19/xxx.jpg}。留空则直接放在 bucket 根目录。
     */
    private String dir = "lost-found";

    /**
     * 自定义访问域名（如 CDN 加速域名）。留空时使用默认域名
     * {@code https://{bucket}.oss-{region}.aliyuncs.com}。
     */
    private String publicBaseUrl;

}
