package com.zzhx.lostfound.system.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.dto.LoginDTO;
import com.zzhx.lostfound.model.dto.PasswordDTO;
import com.zzhx.lostfound.model.dto.ProfileUpdateDTO;
import com.zzhx.lostfound.model.dto.RegisterDTO;
import com.zzhx.lostfound.model.entity.User;
import com.zzhx.lostfound.model.vo.LoginVO;
import com.zzhx.lostfound.model.vo.UserVO;
import jakarta.servlet.http.HttpServletRequest;

import java.util.Map;

/**
 * 用户 Service
 */
public interface UserService extends IService<User> {

    /** 学生实名认证 */
    void verify(Map<String, String> body, Long userId);

    /** 注册 */
    void register(RegisterDTO dto);

    /** 登录，返回 token 与用户信息 */
    LoginVO login(LoginDTO dto);

    /** 登出，使当前 token 失效 */
    void logout(String token);

    Result<UserVO> me(HttpServletRequest request);

    /** 修改个人信息（只允许白名单字段） */
    void updateProfile(ProfileUpdateDTO dto, Long userId);

    /** 判断用户是否为管理员 */
    boolean isAdmin(Long userId);

    /** 修改密码 */
    void updatePassword(PasswordDTO dto, Long userId);
}
