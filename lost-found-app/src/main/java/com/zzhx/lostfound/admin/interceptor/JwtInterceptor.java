package com.zzhx.lostfound.admin.interceptor;

import com.zzhx.lostfound.common.constant.Constants;
import com.zzhx.lostfound.support.JwtService;
import com.zzhx.lostfound.system.security.TokenBlacklist;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.List;

/**
 * JWT 登录拦截器
 */
@Slf4j
@Component
public class JwtInterceptor implements HandlerInterceptor {

    /** 无需登录的白名单（注册、登录） */
    private static final List<String> WHITE_LIST = List.of("/auth/login", "/auth/register");

    private final TokenBlacklist tokenBlacklist;

    private final JwtService jwtService;

    public JwtInterceptor(TokenBlacklist tokenBlacklist, JwtService jwtService) {
        this.tokenBlacklist = tokenBlacklist;
        this.jwtService = jwtService;
    }

    /**
     * 请求前置校验：解析 Authorization 头中的 token，校验通过后把 userId 写入 request 供 Controller 使用
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        // 放行跨域预检请求
        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            return true;
        }
        String uri = request.getRequestURI();
        if (WHITE_LIST.contains(uri)) {
            return true;
        }
        // 公开 GET：物品列表 /items、纯数字详情 /items/{id}、分类列表 /categories
        if ("GET".equalsIgnoreCase(request.getMethod())) {
            if ("/items".equals(uri) || "/categories".equals(uri)) {
                return true;
            }
            if (uri.matches("/items/\\d+")) {
                return true;
            }
        }

        // 其余写操作需要登录
        String header = request.getHeader(Constants.TOKEN_HEADER);
        if (header != null && header.startsWith(Constants.TOKEN_PREFIX)) {
            String token = header.substring(Constants.TOKEN_PREFIX.length());
            try {
                // 登出后的 token 在黑名单中，直接拒绝
                if (tokenBlacklist.contains(token)) {
                    return unauthorized(response);
                }
                Long userId = jwtService.getUserId(token);
                String username = jwtService.getUsername(token);
                request.setAttribute("userId", userId);
                request.setAttribute("username", username);
                return true;
            } catch (Exception e) {
                log.warn("token 解析失败：{}", e.getMessage());
            }
        }
        return unauthorized(response);
    }

    /**
     * 返回 401 未登录响应
     */
    private boolean unauthorized(HttpServletResponse response) throws Exception {
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType("application/json;charset=UTF-8");
        response.getWriter().write("{\"code\":401,\"message\":\"未登录或登录已过期\",\"data\":null}");
        return false;
    }
}
