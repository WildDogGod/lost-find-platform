package com.zzhx.lostfound.system.security;

import org.springframework.stereotype.Component;

import java.util.Iterator;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * 登出 token 黑名单（内存实现）
 *
 * 原理：JWT 是无状态的，服务端默认不保存 token，登出后想让 token 立即失效，
 *       就把它加入黑名单，拦截器每次校验时先查黑名单。
 * 注意：企业生产环境一般使用 Redis（支持分布式、可自动过期），
 *       这里用内存 Map 仅适用于课程设计 / 单机场景，重启后黑名单清空。
 */
@Component
public class TokenBlacklist {

    /** token -> 过期时间戳（毫秒），过期后自动剔除，避免内存无限增长 */
    private final Map<String, Long> blacklist = new ConcurrentHashMap<>();

    /**
     * 加入黑名单
     *
     * @param token    待失效的 token
     * @param expireAt token 自身的过期时间戳
     */
    public void add(String token, long expireAt) {
        if (token == null || token.isBlank()) {
            return;
        }
        blacklist.put(token, expireAt);
        cleanup();
    }

    /**
     * 是否在黑名单中（未过期）
     */
    public boolean contains(String token) {
        if (token == null) {
            return false;
        }
        Long expireAt = blacklist.get(token);
        if (expireAt == null) {
            return false;
        }
        if (expireAt < System.currentTimeMillis()) {
            blacklist.remove(token);
            return false;
        }
        return true;
    }

    /**
     * 清理已过期的 token
     */
    private void cleanup() {
        long now = System.currentTimeMillis();
        Iterator<Map.Entry<String, Long>> iterator = blacklist.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<String, Long> entry = iterator.next();
            if (entry.getValue() < now) {
                blacklist.remove(entry.getKey());
            }
        }
    }
}
