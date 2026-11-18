package com.zzhx.lostfound.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zzhx.lostfound.common.exception.BusinessException;
import com.zzhx.lostfound.common.result.ResultCode;
import com.zzhx.lostfound.model.dto.ClaimDTO;
import com.zzhx.lostfound.model.entity.Claim;
import com.zzhx.lostfound.model.entity.Item;
import com.zzhx.lostfound.system.mapper.ClaimMapper;
import com.zzhx.lostfound.system.service.ClaimService;
import com.zzhx.lostfound.system.service.ItemService;
import com.zzhx.lostfound.system.service.UserService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/**
 * 认领 Service 实现
 */
@Service
public class ClaimServiceImpl extends ServiceImpl<ClaimMapper, Claim> implements ClaimService {

    private final ItemService itemService;

    private final UserService userService;

    public ClaimServiceImpl(ItemService itemService, UserService userService) {
        this.itemService = itemService;
        this.userService = userService;
    }

    /**
     * 提交认领申请：校验物品为招领且有效、非本人发布、无重复待审，并把物品置为处理中
     */
    @Override
    @Transactional
    public void apply(ClaimDTO dto, Long userId) {
        Item item = itemService.getById(dto.getItemId());
        if (item == null) {
            throw new BusinessException(ResultCode.NOT_FOUND);
        }
        if (!"FOUND".equals(item.getType())) {
            throw new BusinessException("只有招领信息可以申请认领");
        }
        if (!"ACTIVE".equals(item.getStatus())) {
            throw new BusinessException("该信息当前不可认领");
        }
        if (Objects.equals(item.getUserId(), userId)) {
            throw new BusinessException("不能认领自己发布的信息");
        }
        Long exists = count(new LambdaQueryWrapper<Claim>()
                .eq(Claim::getItemId, dto.getItemId())
                .eq(Claim::getApplicantId, userId)
                .eq(Claim::getStatus, "PENDING"));
        if (exists > 0) {
            throw new BusinessException("您已提交过认领申请，请勿重复提交");
        }
        Claim claim = new Claim();
        claim.setItemId(dto.getItemId());
        claim.setApplicantId(userId);
        claim.setClaimDesc(dto.getClaimDesc());
        claim.setStatus("PENDING");
        save(claim);

        // 联动：物品进入处理中
        itemService.changeStatus(dto.getItemId(), "PROCESSING");
    }

    /**
     * 查询某个物品的全部认领记录
     */
    @Override
    public List<Claim> listByItem(Long itemId) {
        return list(new LambdaQueryWrapper<Claim>()
                .eq(Claim::getItemId, itemId)
                .orderByDesc(Claim::getCreateTime));
    }

    /**
     * 分页查询当前用户的认领记录
     */
    @Override
    public Page<Claim> mine(Long current, Long size, Long userId) {
        return page(new Page<>(current, size),
                new LambdaQueryWrapper<Claim>()
                        .eq(Claim::getApplicantId, userId)
                        .orderByDesc(Claim::getCreateTime));
    }

    /**
     * 审核认领：校验审核人权限后更新状态，通过时物品标记完成，并发送站内消息
     */
    @Override
    @Transactional
    public void review(Long id, String status, String reviewRemark, Long reviewerId) {
        if (!Set.of("APPROVED", "REJECTED").contains(status)) {
            throw new BusinessException("非法的审核结果");
        }
        Claim claim = getById(id);
        if (claim == null) {
            throw new BusinessException("认领申请不存在");
        }
        if (!"PENDING".equals(claim.getStatus())) {
            throw new BusinessException("该认领申请已处理");
        }
        Item item = itemService.getById(claim.getItemId());
        if (item == null) {
            throw new BusinessException(ResultCode.NOT_FOUND);
        }
        // 只有物品发布者或管理员可以审核
        if (!userService.isAdmin(reviewerId)
                && !Objects.equals(item.getUserId(), reviewerId)) {
            throw new BusinessException(ResultCode.FORBIDDEN);
        }
        if (Objects.equals(claim.getApplicantId(), reviewerId)) {
            throw new BusinessException("不能审核自己的认领申请");
        }
        if ("COMPLETED".equals(item.getStatus()) || "CLOSED".equals(item.getStatus())) {
            throw new BusinessException("物品已结束，无法审核");
        }

        LocalDateTime now = LocalDateTime.now();
        claim.setStatus(status);
        claim.setReviewRemark(reviewRemark);
        claim.setReviewerId(reviewerId);
        claim.setReviewTime(now);
        updateById(claim);

        if ("APPROVED".equals(status)) {
            // 同一物品的其他待处理申请一并驳回
            List<Claim> others = list(new LambdaQueryWrapper<Claim>()
                    .eq(Claim::getItemId, claim.getItemId())
                    .eq(Claim::getStatus, "PENDING")
                    .ne(Claim::getId, claim.getId()));
            for (Claim other : others) {
                other.setStatus("REJECTED");
                other.setReviewRemark("物品已被其他申请人认领");
                other.setReviewerId(reviewerId);
                other.setReviewTime(now);
            }
            if (!others.isEmpty()) {
                updateBatchById(others);
            }
            itemService.changeStatus(claim.getItemId(), "COMPLETED");
        } else {
            // 还有待处理申请则保持处理中，否则重新展示
            Long pending = count(new LambdaQueryWrapper<Claim>()
                    .eq(Claim::getItemId, claim.getItemId())
                    .eq(Claim::getStatus, "PENDING"));
            itemService.changeStatus(claim.getItemId(), pending > 0 ? "PROCESSING" : "ACTIVE");
        }
    }
}
