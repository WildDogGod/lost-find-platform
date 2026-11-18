package com.zzhx.lostfound.system.service;

import org.springframework.web.multipart.MultipartFile;

/**
 * 文件 Service
 */
public interface FileService {

    /** 上传文件，返回可访问的相对 URL */
    String upload(MultipartFile file);
}
