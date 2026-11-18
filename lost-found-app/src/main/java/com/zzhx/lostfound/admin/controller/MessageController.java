package com.zzhx.lostfound.admin.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.zzhx.lostfound.common.result.Result;
import com.zzhx.lostfound.model.dto.MessageDTO;
import com.zzhx.lostfound.model.entity.Message;
import com.zzhx.lostfound.system.service.MessageService;
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

import java.util.Map;

/**
 * 消息接口：发送、列表、已读、未读数
 */
@RestController
@RequestMapping("/messages")
public class MessageController {

    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    /**
     * 发送站内消息，例如向物品发布者留言
     */
    @PostMapping
    public Result<Void> send(@Valid @RequestBody MessageDTO dto, HttpServletRequest request) {
        Long fromUserId = (Long) request.getAttribute("userId");
        messageService.send(dto, fromUserId);
        return Result.success();
    }

    /**
     * 分页查询我收到的消息
     */
    @GetMapping
    public Result<Page<Message>> page(
            @RequestParam(defaultValue = "1") Long current,
            @RequestParam(defaultValue = "10") Long size,
            @RequestParam(required = false) String type,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(messageService.pageQuery(current, size, type, userId));
    }

    /**
     * 把单条消息标记为已读
     */
    @PutMapping("/{id}/read")
    public Result<Void> read(@PathVariable Long id) {
        messageService.markRead(id);
        return Result.success();
    }

    /**
     * 把当前用户全部未读消息标记为已读
     */
    @PutMapping("/read-all")
    public Result<Void> readAll(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        messageService.markAllRead(userId);
        return Result.success();
    }

    /**
     * 查询未读消息数量，供前端红点角标使用
     */
    @GetMapping("/unread-count")
    public Result<Map<String, Object>> unreadCount(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return Result.success(Map.of("count", messageService.unreadCount(userId)));
    }
}
