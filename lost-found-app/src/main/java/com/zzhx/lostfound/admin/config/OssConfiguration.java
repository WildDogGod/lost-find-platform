package com.zzhx.lostfound.admin.config;

import com.zzhx.lostfound.support.AliOssProperties;
import com.zzhx.lostfound.support.AliOssUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 配置类：创建 AliOssUtil 工具类对象。
 * <p>
 * 通过 {@code zzhx.alioss.enabled} 开关控制：默认开启；置为 false 时不创建该 Bean，
 * 文件上传自动退回本地磁盘存储（见 FileServiceImpl）。
 */
@Configuration
@Slf4j
public class OssConfiguration {

    /**
     * 创建阿里云 OSS 上传工具 Bean；当 zzhx.alioss.enabled=false 时不注册，由文件服务回退到本地存储
     */
    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = "zzhx.alioss", name = "enabled", havingValue = "true", matchIfMissing = true)
    public AliOssUtil aliOssUtil(AliOssProperties aliOssProperties) {
        log.info("开始创建阿里云文件上传工具类对象：bucket={}，region={}，dir={}",
                aliOssProperties.getBucketName(), aliOssProperties.getRegion(), aliOssProperties.getDir());
        return new AliOssUtil(aliOssProperties.getRegion(),
                aliOssProperties.getAccessKeyId(),
                aliOssProperties.getAccessKeySecret(),
                aliOssProperties.getBucketName(),
                aliOssProperties.getPublicBaseUrl());
    }
}
