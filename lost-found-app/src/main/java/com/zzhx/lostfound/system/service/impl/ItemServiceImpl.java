package com.zzhx.lostfound.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zzhx.lostfound.common.exception.BusinessException;
import com.zzhx.lostfound.common.result.ResultCode;
import com.zzhx.lostfound.model.dto.ItemDTO;
import com.zzhx.lostfound.model.entity.Item;
import com.zzhx.lostfound.system.mapper.ItemMapper;
import com.zzhx.lostfound.system.service.ItemService;
import com.zzhx.lostfound.system.service.UserService;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.List;
import java.util.Objects;
import java.util.Set;

/**
 * 物品 Service 实现
 */
@Service
public class ItemServiceImpl extends ServiceImpl<ItemMapper, Item> implements ItemService {

    private static final Set<String> ITEM_STATUSES =
            Set.of("PENDING", "ACTIVE", "PROCESSING", "COMPLETED", "CLOSED");

    /** 发布者可以编辑的状态 */
    private static final Set<String> OWNER_EDITABLE =
            Set.of("PENDING", "ACTIVE", "CLOSED");

    /** 发布者可以下架的状态 */
    private static final Set<String> OWNER_CLOSABLE =
            Set.of("PENDING", "ACTIVE");

    private final UserService userService;

    public ItemServiceImpl(UserService userService) {
        this.userService = userService;
    }

    /**
     * 发布物品：归属当前用户，初始状态为 PENDING 待管理员审核
     */
    @Override
    public Long publish(ItemDTO dto, Long userId) {
        Item item = new Item();
        BeanUtils.copyProperties(dto, item);
        item.setUserId(userId);
        item.setStatus("PENDING");
        save(item);
        return item.getId();
    }

    /**
     * 多条件分页查询：类型、分类、关键词（标题/描述）、地点、状态，按发布时间倒序
     */
    @Override
    public Page<Item> pageQuery(Long current, Long size, String type, Long categoryId,
                                String keyword, String location, String status) {
        LambdaQueryWrapper<Item> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(StringUtils.hasText(type), Item::getType, type);
        wrapper.eq(categoryId != null, Item::getCategoryId, categoryId);
        if (StringUtils.hasText(keyword)) {
            wrapper.and(w -> w.like(Item::getTitle, keyword)
                    .or().like(Item::getDescription, keyword));
        }
        wrapper.like(StringUtils.hasText(location), Item::getLocation, location);
        wrapper.eq(StringUtils.hasText(status), Item::getStatus, status);
        wrapper.orderByDesc(Item::getCreateTime);
        return page(new Page<>(current, size), wrapper);
    }

    /**
     * 编辑物品：校验归属关系与当前状态是否允许修改
     */
    @Override
    public void updateItem(Long id, ItemDTO dto, Long operatorId) {
        Item existing = requireItem(id);
        boolean admin = userService.isAdmin(operatorId);
        if (!admin) {
            requireOwner(existing, operatorId);
            if (!OWNER_EDITABLE.contains(existing.getStatus())) {
                throw new BusinessException("当前状态不可编辑");
            }
        }
        Item item = new Item();
        BeanUtils.copyProperties(dto, item);
        item.setId(id);
        if (!admin) {
            // 已通过审核的内容被修改后必须重新审核，防止审核后篡改
            item.setStatus("PENDING");
            item.setAuditRemark("");
        }
        updateById(item);
    }

    /**
     * 删除物品：仅发布者本人或管理员，处理中与已完成的物品不可删
     */
    @Override
    public void deleteItem(Long id, Long operatorId) {
        Item item = requireItem(id);
        if (!userService.isAdmin(operatorId)) {
            requireOwner(item, operatorId);
        }
        removeById(id);
    }

    /**
     * 变更物品状态：校验状态合法性以及操作权限
     */
    @Override
    public void updateStatus(Long id, String status, Long operatorId) {
        Item item = requireItem(id);
        if (!ITEM_STATUSES.contains(status)) {
            throw new BusinessException("非法的物品状态");
        }
        if (!userService.isAdmin(operatorId)) {
            requireOwner(item, operatorId);
            if (!"CLOSED".equals(status)) {
                throw new BusinessException("只能下架自己发布的信息");
            }
            if (!OWNER_CLOSABLE.contains(item.getStatus())) {
                throw new BusinessException("当前状态不可下架");
            }
        }
        changeStatus(id, status);
    }

    /**
     * 内部状态流转方法，供认领流程联动调用
     */
    @Override
    public void changeStatus(Long id, String status) {
        if (!ITEM_STATUSES.contains(status)) {
            throw new BusinessException("非法的物品状态");
        }
        Item item = new Item();
        item.setId(id);
        item.setStatus(status);
        updateById(item);
    }

    private Item requireItem(Long id) {
        Item item = getById(id);
        if (item == null) {
            throw new BusinessException(ResultCode.NOT_FOUND);
        }
        return item;
    }

    private void requireOwner(Item item, Long operatorId) {
        if (!Objects.equals(item.getUserId(), operatorId)) {
            throw new BusinessException(ResultCode.FORBIDDEN);
        }
    }

    /**
     * 分页查询我发布的物品，可按类型筛选
     */
    @Override
    public Page<Item> mine(Long current, Long size, String type, Long userId) {
        LambdaQueryWrapper<Item> wrapper = new LambdaQueryWrapper<Item>()
                .eq(Item::getUserId, userId)
                .eq(StringUtils.hasText(type), Item::getType, type)
                .orderByDesc(Item::getCreateTime);
        return page(new Page<>(current, size), wrapper);
    }

    /**
     * 智能匹配：类型相反、同分类且状态为 ACTIVE，按发生时间倒序
     */
    @Override
    public List<Item> matches(Long id) {
        Item item = getById(id);
        if (item == null) {
            throw new BusinessException("物品不存在");
        }
        String oppositeType = "LOST".equals(item.getType()) ? "FOUND" : "LOST";
        LambdaQueryWrapper<Item> wrapper = new LambdaQueryWrapper<Item>()
                .eq(Item::getType, oppositeType)
                .eq(Item::getCategoryId, item.getCategoryId())
                .eq(Item::getStatus, "ACTIVE")
                .orderByDesc(Item::getEventTime);
        return list(wrapper);
    }
}
