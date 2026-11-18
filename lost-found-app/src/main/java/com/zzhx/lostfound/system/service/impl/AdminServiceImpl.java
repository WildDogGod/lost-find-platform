package com.zzhx.lostfound.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.zzhx.lostfound.common.exception.BusinessException;
import com.zzhx.lostfound.common.result.ResultCode;
import com.zzhx.lostfound.model.entity.Category;
import com.zzhx.lostfound.model.entity.Item;
import com.zzhx.lostfound.model.entity.User;
import com.zzhx.lostfound.model.vo.StatsVO;
import com.zzhx.lostfound.system.service.AdminService;
import com.zzhx.lostfound.system.service.CategoryService;
import com.zzhx.lostfound.system.service.ItemService;
import com.zzhx.lostfound.system.service.UserService;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * 管理员 Service 实现
 */
@Service
public class AdminServiceImpl implements AdminService {

    private final ItemService itemService;

    private final UserService userService;

    private final CategoryService categoryService;

    public AdminServiceImpl(ItemService itemService, UserService userService,
                            CategoryService categoryService) {
        this.itemService = itemService;
        this.userService = userService;
        this.categoryService = categoryService;
    }

    /** 校验当前登录用户是否为管理员 */
    private void checkAdmin(Long userId) {
        User user = userService.getById(userId);
        if (user == null || !"ADMIN".equals(user.getRole())) {
            throw new BusinessException(ResultCode.FORBIDDEN);
        }
    }

    /**
     * 管理员视角分页查询全部物品，包含待审核与已结束的
     */
    @Override
    public Page<Item> itemPage(Long current, Long size, String status, String type, Long userId) {
        checkAdmin(userId);
        LambdaQueryWrapper<Item> wrapper = new LambdaQueryWrapper<Item>()
                .eq(StringUtils.hasText(status), Item::getStatus, status)
                .eq(StringUtils.hasText(type), Item::getType, type)
                .orderByDesc(Item::getCreateTime);
        return itemService.page(new Page<>(current, size), wrapper);
    }

    /**
     * 审核物品：写入审核备注，并按审核结果变更状态
     */
    @Override
    public void audit(Long id, String status, String auditRemark, Long userId) {
        checkAdmin(userId);
        if (!Set.of("ACTIVE", "CLOSED").contains(status)) {
            throw new BusinessException("非法的审核结果");
        }
        Item existing = itemService.getById(id);
        if (existing == null) {
            throw new BusinessException(ResultCode.NOT_FOUND);
        }
        if (!"PENDING".equals(existing.getStatus())) {
            throw new BusinessException("只有待审核信息可以审核");
        }
        Item item = new Item();
        item.setId(id);
        item.setStatus(status);
        item.setAuditRemark(auditRemark);
        itemService.updateById(item);
    }

    /**
     * 分页查询用户列表
     */
    @Override
    public Page<User> userPage(Long current, Long size, String keyword, Long userId) {
        checkAdmin(userId);
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        if (StringUtils.hasText(keyword)) {
            wrapper.and(w -> w.like(User::getUsername, keyword)
                    .or().like(User::getRealName, keyword)
                    .or().like(User::getStudentNo, keyword));
        }
        wrapper.orderByDesc(User::getCreateTime);
        return userService.page(new Page<>(current, size), wrapper);
    }

    /**
     * 更新用户状态，正常或封禁
     */
    @Override
    public void updateUserStatus(Long id, Integer status, Long userId) {
        checkAdmin(userId);
        User user = new User();
        user.setId(id);
        user.setStatus(status);
        userService.updateById(user);
    }

    /**
     * 聚合统计：各状态数量、完成成功率与分类分布
     */
    @Override
    public StatsVO stats(Long userId) {
        checkAdmin(userId);
        StatsVO stats = new StatsVO();
        stats.setTotalUsers(userService.count());
        stats.setTotalItems(itemService.count());
        stats.setLostCount(itemService.count(new LambdaQueryWrapper<Item>().eq(Item::getType, "LOST")));
        stats.setFoundCount(itemService.count(new LambdaQueryWrapper<Item>().eq(Item::getType, "FOUND")));
        stats.setCompletedCount(itemService.count(new LambdaQueryWrapper<Item>()
                .eq(Item::getStatus, "COMPLETED")));
        stats.setSuccessRate(stats.getTotalItems() == 0
                ? 0.0
                : (double) stats.getCompletedCount() / stats.getTotalItems());

        List<Category> categories = categoryService.list();
        List<StatsVO.CategoryCount> distribution = new ArrayList<>();
        for (Category category : categories) {
            StatsVO.CategoryCount count = new StatsVO.CategoryCount();
            count.setCategoryName(category.getName());
            count.setCount(itemService.count(new LambdaQueryWrapper<Item>()
                    .eq(Item::getCategoryId, category.getId())));
            distribution.add(count);
        }
        stats.setCategoryDistribution(distribution);
        return stats;
    }
}
