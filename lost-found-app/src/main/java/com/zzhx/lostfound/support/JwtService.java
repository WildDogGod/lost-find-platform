package com.zzhx.lostfound.support;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT 服务。
 *
 * <p>密钥来自配置项 {@code zzhx.jwt.secret}，不再硬编码在代码里；
 * 生产环境通过环境变量 JWT_SECRET 或外部配置文件注入。</p>
 */
@Component
public class JwtService {

    private final SecretKey key;

    private final long expirationMillis;

    public JwtService(@Value("${zzhx.jwt.secret}") String secret,
                      @Value("${zzhx.jwt.expiration-minutes:1440}") long expirationMinutes) {
        if (secret == null || secret.getBytes(StandardCharsets.UTF_8).length < 32) {
            throw new IllegalStateException("zzhx.jwt.secret 未配置或长度不足 32 字节");
        }
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.expirationMillis = expirationMinutes * 60 * 1000;
    }

    /**
     * 生成 token
     */
    public String generateToken(Long userId, String username) {
        Date now = new Date();
        Date expireDate = new Date(now.getTime() + expirationMillis);
        return Jwts.builder()
                .subject(username)
                .claim("userId", userId)
                .claim("username", username)
                .issuedAt(now)
                .expiration(expireDate)
                .signWith(key)
                .compact();
    }

    /**
     * 解析 token
     */
    public Claims parseToken(String token) {
        return Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    /**
     * 从 token 中获取用户 ID
     */
    public Long getUserId(String token) {
        Object userId = parseToken(token).get("userId");
        return userId == null ? null : Long.valueOf(userId.toString());
    }

    /**
     * 从 token 中获取用户名
     */
    public String getUsername(String token) {
        return parseToken(token).get("username", String.class);
    }

    /**
     * 获取 token 的过期时间戳（毫秒）
     */
    public long getExpireAt(String token) {
        return parseToken(token).getExpiration().getTime();
    }
}
