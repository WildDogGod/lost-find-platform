package com.zzhx.lostfound.system.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.zzhx.lostfound.model.entity.Item;
import com.zzhx.lostfound.model.entity.User;
import com.zzhx.lostfound.model.vo.StatsVO;

/**
 * 管理员 Service
 */
public interface AdminService {

    /** 物品分页（后台） */
    Page<Item> itemPage(Long current, Long size, String status, String type, Long userId);

    /** 物品审核 */
    void audit(Long id, String status, String auditRemark, Long userId);

    /** 用户分页（后台） */
    Page<User> userPage(Long current, Long size, String keyword, Long userId);

    /** 启用 / 封禁用户 */
    void updateUserStatus(Long id, Integer status, Long userId);

    /** 数据统计 */
    StatsVO stats(Long userId);
}
