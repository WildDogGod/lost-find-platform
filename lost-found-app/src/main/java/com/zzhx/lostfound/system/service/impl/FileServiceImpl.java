package com.zzhx.lostfound.system.service.impl;

import com.zzhx.lostfound.common.exception.BusinessException;
import com.zzhx.lostfound.support.AliOssProperties;
import com.zzhx.lostfound.support.AliOssUtil;
import com.zzhx.lostfound.system.service.FileService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/**
 * 文件 Service 实现。
 * <p>
 * 优先走阿里云 OSS（{@link AliOssUtil} 由 OssConfiguration 创建，受 zzhx.alioss.enabled 控制），
 * 上传成功后返回 OSS 的完整访问地址，前端直接用该地址显示图片；
 * 当 OSS 被关闭（未创建 Bean）时退回本地磁盘存储，返回 {@code /upload/...} 相对地址。
 */
@Slf4j
@Service
public class FileServiceImpl implements FileService {

    /** OSS 对象名中的日期目录：2026/10/19/xxx.jpg */
    private static final DateTimeFormatter OSS_DATE_DIR = DateTimeFormatter.ofPattern("yyyy/MM/dd");

    /** 本地存储的日期目录：20261019 */
    private static final DateTimeFormatter LOCAL_DATE_DIR = DateTimeFormatter.ofPattern("yyyyMMdd");

    /** 允许上传的图片类型（该上传接口只服务于物品图片 / 头像） */
    private static final Set<String> ALLOWED_CONTENT_TYPES = Set.of(
            "image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp");

    /** 扩展名 -> Content-Type，防止浏览器上传时 content-type 缺失或为 octet-stream */
    private static final Map<String, String> EXTENSION_CONTENT_TYPES = Map.of(
            ".jpg", "image/jpeg",
            ".jpeg", "image/jpeg",
            ".png", "image/png",
            ".gif", "image/gif",
            ".webp", "image/webp",
            ".bmp", "image/bmp");

    private final AliOssUtil aliOssUtil;
    private final AliOssProperties aliOssProperties;

    public FileServiceImpl(ObjectProvider<AliOssUtil> aliOssUtilProvider,
                           AliOssProperties aliOssProperties) {
        this.aliOssUtil = aliOssUtilProvider.getIfAvailable();
        this.aliOssProperties = aliOssProperties;
        if (aliOssUtil == null) {
            log.warn("未启用阿里云 OSS（zzhx.alioss.enabled=false），文件将上传到本地磁盘");
        }
    }

    /**
     * 上传文件：启用 OSS 时上传云端返回外链，否则保存到本地 upload 目录
     */
    @Override
    public String upload(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new BusinessException("上传文件不能为空");
        }
        String extension = resolveExtension(file.getOriginalFilename());
        if (!EXTENSION_CONTENT_TYPES.containsKey(extension)) {
            throw new BusinessException("仅支持上传 jpg / jpeg / png / gif / webp / bmp 图片");
        }
        String contentType = resolveContentType(file.getContentType(), extension);
        String fileName = UUID.randomUUID().toString().replace("-", "") + extension;
        return aliOssUtil != null
                ? uploadToOss(file, fileName, contentType)
                : uploadToLocal(file, fileName);
    }

    private String uploadToOss(MultipartFile file, String fileName, String contentType) {
        String objectName = buildObjectName(fileName);
        try {
            return aliOssUtil.upload(file.getBytes(), objectName, contentType);
        } catch (IOException e) {
            throw new BusinessException("读取上传文件失败：" + e.getMessage());
        }
    }

    /**
     * 对象名 = 配置目录（zzhx.alioss.dir）+ 日期 + 文件名，
     * 例如 lost-found/2026/10/19/0de5....png。
     */
    private String buildObjectName(String fileName) {
        String dir = aliOssProperties.getDir() == null ? "" : aliOssProperties.getDir().trim();
        while (dir.startsWith("/")) {
            dir = dir.substring(1);
        }
        while (dir.endsWith("/")) {
            dir = dir.substring(0, dir.length() - 1);
        }
        String datePath = LocalDate.now().format(OSS_DATE_DIR);
        String prefix = dir.isEmpty() ? datePath : dir + "/" + datePath;
        return prefix + "/" + fileName;
    }

    private String uploadToLocal(MultipartFile file, String fileName) {
        String datePath = LocalDate.now().format(LOCAL_DATE_DIR);
        File folder = new File(System.getProperty("user.dir") + "/upload/" + datePath);
        if (!folder.exists() && !folder.mkdirs()) {
            throw new BusinessException("创建上传目录失败");
        }
        try {
            file.transferTo(new File(folder, fileName));
        } catch (IOException e) {
            throw new BusinessException("文件上传失败：" + e.getMessage());
        }
        return "/upload/" + datePath + "/" + fileName;
    }

    /**
     * 从原始文件名中取出扩展名（统一转小写）。
     * 只接受「点 + 1~10 位字母数字」，避免把路径分隔符、查询串等带进对象名。
     */
    private String resolveExtension(String originalFilename) {
        if (originalFilename == null) {
            return ".jpg";
        }
        int dot = originalFilename.lastIndexOf('.');
        if (dot < 0 || dot == originalFilename.length() - 1) {
            return ".jpg";
        }
        String ext = originalFilename.substring(dot).toLowerCase(Locale.ROOT);
        return ext.matches("\\.[a-z0-9]{1,10}") ? ext : ".jpg";
    }

    /**
     * 优先使用浏览器上报的 image/* 类型；否则按扩展名补齐，保证 OSS 对象可内联显示。
     */
    private String resolveContentType(String contentType, String extension) {
        if (contentType != null && ALLOWED_CONTENT_TYPES.contains(contentType.toLowerCase(Locale.ROOT))) {
            return contentType.toLowerCase(Locale.ROOT);
        }
        return EXTENSION_CONTENT_TYPES.getOrDefault(extension, "image/jpeg");
    }
}
