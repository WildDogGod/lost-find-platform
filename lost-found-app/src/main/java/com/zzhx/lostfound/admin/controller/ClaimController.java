package com.zzhx.lostfound.admin.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.zzhx.lostfound.common.annotation.Log;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.dto.ClaimDTO;
import com.zzhx.lostfound.model.entity.Claim;
import com.zzhx.lostfound.system.service.ClaimService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

/**
 * 认领接口：申请、审核、记录
 */
@RestController
@RequestMapping("/claims")
public class ClaimController {

    private final ClaimService claimService;

    public ClaimController(ClaimService claimService) {
        this.claimService = claimService;
    }

    /**
     * 提交认领申请：校验物品可认领，并记录认领凭证
     */
    @Log("提交认领申请")
    @PostMapping
    public Result<Void> apply(@Valid @RequestBody ClaimDTO dto, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        claimService.apply(dto, userId);
        return Result.success();
    }

    /**
     * 查询某个物品下的全部认领申请，供发布者查看谁在认领
     */
    @GetMapping("/item/{itemId}")
    public Result<List<Claim>> itemClaims(@PathVariable Long itemId) {
        return Result.success(claimService.listByItem(itemId));
    }

    /**
     * 分页查询当前用户提交过的认领申请
     */
    @GetMapping("/mine")
    public Result<Page<Claim>> mine(
            @RequestParam(defaultValue = "1") Long current,
            @RequestParam(defaultValue = "10") Long size,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(claimService.mine(current, size, userId));
    }

    /**
     * 审核认领申请：通过则物品标记完成，驳回则恢复可认领，并通知申请人
     */
    @Log("审核认领申请")
    @PutMapping("/{id}/review")
    public Result<Void> review(@PathVariable Long id, @RequestBody Map<String, String> body,
                               HttpServletRequest request) {
        Long reviewerId = (Long) request.getAttribute("userId");
        claimService.review(id, body.get("status"), body.get("reviewRemark"), reviewerId);
        return Result.success();
    }
}
