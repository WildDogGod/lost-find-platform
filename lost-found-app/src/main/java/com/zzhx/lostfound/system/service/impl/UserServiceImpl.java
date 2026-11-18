package com.zzhx.lostfound.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zzhx.lostfound.common.constant.Constants;
import com.zzhx.lostfound.common.exception.BusinessException;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.support.JwtService;
import com.zzhx.lostfound.model.dto.LoginDTO;
import com.zzhx.lostfound.model.dto.PasswordDTO;
import com.zzhx.lostfound.model.dto.ProfileUpdateDTO;
import com.zzhx.lostfound.model.dto.RegisterDTO;
import com.zzhx.lostfound.model.entity.User;
import com.zzhx.lostfound.model.vo.LoginVO;
import com.zzhx.lostfound.model.vo.UserVO;
import com.zzhx.lostfound.system.mapper.UserMapper;
import com.zzhx.lostfound.system.security.TokenBlacklist;
import com.zzhx.lostfound.system.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.BeanUtils;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Map;

/**
 * 用户 Service 实现
 */
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    private final PasswordEncoder passwordEncoder;

    private final TokenBlacklist tokenBlacklist;

    private final JwtService jwtService;

    public UserServiceImpl(PasswordEncoder passwordEncoder, TokenBlacklist tokenBlacklist,
                           JwtService jwtService) {
        this.passwordEncoder = passwordEncoder;
        this.tokenBlacklist = tokenBlacklist;
        this.jwtService = jwtService;
    }

    /**
     * 提交实名认证：保存学号与姓名并更新认证状态
     */
    @Override
    public void verify(Map<String, String> body, Long userId) {
        User update = new User();
        update.setId(userId);
        update.setRealName(body.get("realName"));
        update.setStudentNo(body.get("studentNo"));
        update.setCollege(body.get("college"));
        update.setVerifyStatus(1);
        updateById(update);
    }

    /**
     * 注册：校验用户名唯一，密码用 BCrypt 加密，默认 USER 角色
     */
    @Override
    public void register(RegisterDTO dto) {
        // 校验用户名唯一
        Long count = count(new LambdaQueryWrapper<User>()
                .eq(User::getUsername, dto.getUsername()));
        if (count > 0) {
            throw new BusinessException("用户已存在");
        }
        User user = new User();
        BeanUtils.copyProperties(dto, user);
        user.setPassword(passwordEncoder.encode(dto.getPassword()));
        user.setRole(Constants.ROLE_USER);
        user.setVerifyStatus(0);
        user.setStatus(0);
        save(user);
    }

    /**
     * 登录：校验账号状态与密码，成功后签发 JWT
     */
    @Override
    public LoginVO login(LoginDTO dto) {
        User user = getOne(new LambdaQueryWrapper<User>()
                .eq(User::getUsername, dto.getUsername()));
        if (user == null || !passwordEncoder.matches(dto.getPassword(), user.getPassword())) {
            throw new BusinessException("账号或密码错误");
        }
        if (user.getStatus() != null && user.getStatus() == 1) {
            throw new BusinessException("账号已被封禁");
        }
        String token = jwtService.generateToken(user.getId(), user.getUsername());

        LoginVO vo = new LoginVO();
        vo.setToken(token);
        UserVO userVO = new UserVO();
        BeanUtils.copyProperties(user, userVO);
        vo.setUserInfo(userVO);
        return vo;
    }

    /**
     * 退出登录：把当前 token 放入黑名单
     */
    @Override
    public void logout(String token) {
        if (token == null || token.isBlank()) {
            throw new BusinessException("未登录，无需退出");
        }
        // 加入黑名单，让 token 立即失效
        tokenBlacklist.add(token, jwtService.getExpireAt(token));
    }

    /**
     * 查询当前登录用户信息，密码等敏感字段不返回
     */
    @Override
    public Result<UserVO> me(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        User user = getById(userId);
        UserVO vo = new UserVO();
        BeanUtils.copyProperties(user, vo);
        return Result.success(vo);
    }

    /**
     * 更新个人资料
     */
    @Override
    public void updateProfile(ProfileUpdateDTO dto, Long userId) {
        User user = getById(userId);
        if (user == null) {
            throw new BusinessException("用户不存在");
        }
        // 显式赋值：role、status、verifyStatus、username 等字段不允许客户端修改
        User update = new User();
        update.setId(userId);
        update.setRealName(dto.getRealName());
        update.setPhone(dto.getPhone());
        update.setEmail(dto.getEmail());
        update.setAvatar(dto.getAvatar());
        updateById(update);
    }

    /**
     * 判断用户是否为管理员，认领审核等场景据此放行
     */
    @Override
    public boolean isAdmin(Long userId) {
        if (userId == null) {
            return false;
        }
        User user = getById(userId);
        return user != null && Constants.ROLE_ADMIN.equals(user.getRole());
    }

    /**
     * 修改密码：校验旧密码后把新密码重新加密保存
     */
    @Override
    public void updatePassword(PasswordDTO dto, Long userId) {
        // 校验两次新密码一致
        if (!dto.getNewPassword().equals(dto.getConfirmPassword())) {
            throw new BusinessException("两次输入的新密码不一致");
        }
        User user = getById(userId);
        if (user == null) {
            throw new BusinessException("用户不存在");
        }
        // 校验原密码是否正确
        if (!passwordEncoder.matches(dto.getOldPassword(), user.getPassword())) {
            throw new BusinessException("原密码错误");
        }
        // 新密码不能与原密码相同
        if (passwordEncoder.matches(dto.getNewPassword(), user.getPassword())) {
            throw new BusinessException("新密码不能与原密码相同");
        }
        User update = new User();
        update.setId(userId);
        update.setPassword(passwordEncoder.encode(dto.getNewPassword()));
        updateById(update);
    }
}
