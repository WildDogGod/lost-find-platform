package com.zzhx.lostfound;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 校园失物招领平台启动类
 */
@MapperScan("com.zzhx.lostfound.system.mapper")
@SpringBootApplication
public class LostFoundPlatformApplication {

    public static void main(String[] args) {
        SpringApplication.run(LostFoundPlatformApplication.class, args);
    }
}
