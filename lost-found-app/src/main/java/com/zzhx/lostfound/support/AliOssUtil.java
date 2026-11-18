package com.zzhx.lostfound.support;

import com.aliyun.sdk.service.oss2.OSSClient;
import com.aliyun.sdk.service.oss2.credentials.StaticCredentialsProvider;
import com.aliyun.sdk.service.oss2.exceptions.ServiceException;
import com.aliyun.sdk.service.oss2.models.PutObjectRequest;
import com.aliyun.sdk.service.oss2.transport.BinaryData;
import com.zzhx.lostfound.common.exception.BusinessException;
import jakarta.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;

/**
 * 阿里云 OSS 文件上传工具（基于 alibabacloud-oss-v2 SDK）
 * OSSClient 线程安全，全局只构建一次，随 Spring 容器关闭释放
 */
@Slf4j
public class AliOssUtil {

    private final String region;
    private final String accessKeyId;
    private final String accessKeySecret;
    private final String bucketName;
    private final String publicBaseUrl;
    private final OSSClient ossClient;

    public AliOssUtil(String region, String accessKeyId, String accessKeySecret,
                      String bucketName, String publicBaseUrl) {
        this.region = region;
        this.accessKeyId = accessKeyId;
        this.accessKeySecret = accessKeySecret;
        this.bucketName = bucketName;
        this.publicBaseUrl = publicBaseUrl == null ? "" : publicBaseUrl.trim();
        // V2 SDK 必须用 region 进行 V4 签名（只设 endpoint 会报 Invalid signing region）
        this.ossClient = OSSClient.newBuilder()
                .region(region)
                .credentialsProvider(new StaticCredentialsProvider(accessKeyId, accessKeySecret))
                .build();
        log.info("阿里云OSS客户端初始化完成：region={}，bucket={}", region, bucketName);
    }

    /**
     * 上传文件
     *
     * @param bytes      文件字节数组
     * @param objectName 对象名（含目录，如 2026/10/19/xxxxx.jpg）
     * @return 文件可访问的完整 URL
     */
    public String upload(byte[] bytes, String objectName) {
        return upload(bytes, objectName, null);
    }

    /**
     * 上传文件，并显式指定 Content-Type。
     * <p>
     * 不指定时 OSS 会存成 application/octet-stream，浏览器直接打开图片地址会变成下载；
     * 指定成 image/jpeg 等类型后 {@code <img>} / el-image 才能正常内联显示。
     *
     * @param contentType 文件 MIME 类型，为空时由 OSS 自行判断
     */
    public String upload(byte[] bytes, String objectName, String contentType) {
        try {
            PutObjectRequest.Builder builder = PutObjectRequest.newBuilder()
                    .bucket(bucketName)
                    .key(objectName)
                    .body(BinaryData.fromBytes(bytes));
            if (contentType != null && !contentType.isBlank()) {
                builder.contentType(contentType);
            }
            ossClient.putObject(builder.build());
        } catch (ServiceException e) {
            // 请求到达 OSS 但被拒绝（AK错误、无权限、bucket不存在、地域不对等）
            log.error("OSS上传被拒绝：errorCode={}，message={}，requestId={}",
                    e.errorCode(), e.errorMessage(), e.requestId());
            throw new BusinessException("文件上传失败：" + e.errorMessage());
        } catch (Exception e) {
            // 网络不通、无法连接等客户端异常
            log.error("OSS上传发生异常：", e);
            throw new BusinessException("文件上传失败：" + e.getMessage());
        }

        String url = buildUrl(objectName);
        log.info("文件上传到：{}", url);
        return url;
    }

    /**
     * 访问路径：优先使用配置的自定义域名，否则用
     * {@code https://BucketName.oss-region.aliyuncs.com/ObjectName}。
     */
    private String buildUrl(String objectName) {
        String base = publicBaseUrl;
        if (base.isEmpty()) {
            base = "https://" + bucketName + ".oss-" + region + ".aliyuncs.com";
        }
        while (base.endsWith("/")) {
            base = base.substring(0, base.length() - 1);
        }
        return base + "/" + objectName;
    }

    /**
     * 容器关闭时释放 OSS 客户端连接
     */
    @PreDestroy
    public void shutdown() {
        if (ossClient != null) {
            try {
                ossClient.close();
            } catch (Exception e) {
                log.warn("关闭OSS客户端异常：{}", e.getMessage());
            }
        }
    }
}
