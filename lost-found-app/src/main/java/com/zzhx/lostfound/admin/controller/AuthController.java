package com.zzhx.lostfound.admin.controller;

import com.zzhx.lostfound.common.constant.Constants;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.dto.LoginDTO;
import com.zzhx.lostfound.model.dto.RegisterDTO;
import com.zzhx.lostfound.model.vo.LoginVO;
import com.zzhx.lostfound.system.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 认证接口：注册、登录、登出
 */
@RestController
@RequestMapping("/auth")
public class AuthController {

    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    /**
     * 用户注册：校验用户名唯一，密码经 BCrypt 加密后入库
     */
    @PostMapping("/register")
    public Result<Void> register(@Valid @RequestBody RegisterDTO dto) {
        userService.register(dto);
        return Result.success();
    }

    /**
     * 登录：校验账号密码，成功后签发 JWT 并返回用户信息
     */
    @PostMapping("/login")
    public Result<LoginVO> login(@Valid @RequestBody LoginDTO dto) {
        return Result.success(userService.login(dto));
    }

    /**
     * 退出登录：把当前 token 加入黑名单，使其立即失效
     */
    @PostMapping("/logout")
    public Result<Void> logout(HttpServletRequest request) {
        String header = request.getHeader(Constants.TOKEN_HEADER);
        String token = null;
        if (header != null && header.startsWith(Constants.TOKEN_PREFIX)) {
            token = header.substring(Constants.TOKEN_PREFIX.length());
        }
        userService.logout(token);
        return Result.success();
    }
}
