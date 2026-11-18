package com.zzhx.lostfound.admin.controller;

import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.dto.PasswordDTO;
import com.zzhx.lostfound.model.dto.ProfileUpdateDTO;
import com.zzhx.lostfound.model.vo.UserVO;
import com.zzhx.lostfound.system.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 用户接口：个人信息、密码、学生认证
 */
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    /**
     * 获取当前登录用户的完整信息
     */
    @GetMapping("/me")
    public Result<UserVO> me(HttpServletRequest request) {
        return userService.me(request);
    }

    /**
     * 更新个人资料，如姓名、学院、联系方式
     */
    @PutMapping("/me")
    public Result<Void> update(@Valid @RequestBody ProfileUpdateDTO dto, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        userService.updateProfile(dto, userId);
        return Result.success();
    }

    /**
     * 修改密码：校验旧密码后重新加密保存
     */
    @PutMapping("/password")
    public Result<Void> updatePassword(@Valid @RequestBody PasswordDTO dto, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        userService.updatePassword(dto, userId);
        return Result.success();
    }

    /**
     * 提交校园实名认证，保存学号与姓名
     */
    @PostMapping("/verify")
    public Result<Void> verify(@RequestBody Map<String, String> body, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        userService.verify(body, userId);
        return Result.success();
    }
}
