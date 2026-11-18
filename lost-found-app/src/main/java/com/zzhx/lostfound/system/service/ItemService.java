package com.zzhx.lostfound.system.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.zzhx.lostfound.model.dto.ItemDTO;
import com.zzhx.lostfound.model.entity.Item;

import java.util.List;

/**
 * 物品 Service
 */
public interface ItemService extends IService<Item> {

    /** 发布物品，返回物品 ID */
    Long publish(ItemDTO dto, Long userId);

    /** 分页条件查询 */
    Page<Item> pageQuery(Long current, Long size, String type, Long categoryId,
                         String keyword, String location, String status);

    /** 更新物品（仅发布者或管理员） */
    void updateItem(Long id, ItemDTO dto, Long operatorId);

    /** 删除物品（仅发布者或管理员） */
    void deleteItem(Long id, Long operatorId);

    /** 发布者下架物品 */
    void updateStatus(Long id, String status, Long operatorId);

    /** 内部状态流转（认领审核等业务使用，不做用户权限判断） */
    void changeStatus(Long id, String status);

    /** 我的发布 */
    Page<Item> mine(Long current, Long size, String type, Long userId);

    /** 智能匹配（同分类、相反类型、展示中） */
    List<Item> matches(Long id);
}
