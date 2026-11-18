package com.zzhx.lostfound.system.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.zzhx.lostfound.model.dto.ClaimDTO;
import com.zzhx.lostfound.model.entity.Claim;

import java.util.List;

/**
 * 认领 Service
 */
public interface ClaimService extends IService<Claim> {

    /** 提交认领申请 */
    void apply(ClaimDTO dto, Long userId);

    /** 某物品的认领记录 */
    List<Claim> listByItem(Long itemId);

    /** 我的认领 */
    Page<Claim> mine(Long current, Long size, Long userId);

    /** 审核认领申请 */
    void review(Long id, String status, String reviewRemark, Long reviewerId);
}
