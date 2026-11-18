package com.zzhx.lostfound.admin.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.entity.Item;
import com.zzhx.lostfound.model.entity.User;
import com.zzhx.lostfound.model.vo.StatsVO;
import com.zzhx.lostfound.system.service.AdminService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 管理员接口：审核、用户管理、统计
 */
@RestController
@RequestMapping("/admin")
public class AdminController {

    private final AdminService adminService;

    public AdminController(AdminService adminService) {
        this.adminService = adminService;
    }

    /**
     * 管理员分页查询全部物品（含待审核），支持按状态、关键词筛选
     */
    @GetMapping("/items")
    public Result<Page<Item>> items(
            @RequestParam(defaultValue = "1") Long current,
            @RequestParam(defaultValue = "10") Long size,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String type,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(adminService.itemPage(current, size, status, type, userId));
    }

    /**
     * 审核物品信息：通过则上架为 ACTIVE，驳回则记录审核备注
     */
    @PutMapping("/items/{id}/audit")
    public Result<Void> audit(@PathVariable Long id, @RequestBody Map<String, String> body,
                              HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        adminService.audit(id, body.get("status"), body.get("auditRemark"), userId);
        return Result.success();
    }

    /**
     * 管理员分页查询用户，支持按用户名、状态筛选
     */
    @GetMapping("/users")
    public Result<Page<User>> users(
            @RequestParam(defaultValue = "1") Long current,
            @RequestParam(defaultValue = "10") Long size,
            @RequestParam(required = false) String keyword,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(adminService.userPage(current, size, keyword, userId));
    }

    /**
     * 启用或封禁用户账号（0 正常 / 1 封禁）
     */
    @PutMapping("/users/{id}/status")
    public Result<Void> updateUserStatus(@PathVariable Long id, @RequestBody Map<String, Integer> body,
                                         HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        adminService.updateUserStatus(id, body.get("status"), userId);
        return Result.success();
    }

    /**
     * 平台数据统计：用户数、物品数、寻物/招领数、完成率与分类分布
     */
    @GetMapping("/stats")
    public Result<StatsVO> stats(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(adminService.stats(userId));
    }
}
