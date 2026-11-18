package com.zzhx.lostfound.system.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.zzhx.lostfound.model.dto.MessageDTO;
import com.zzhx.lostfound.model.entity.Message;

/**
 * 消息 Service
 */
public interface MessageService extends IService<Message> {

    /** 发送留言 */
    void send(MessageDTO dto, Long fromUserId);

    /** 分页查询收到的消息 */
    Page<Message> pageQuery(Long current, Long size, String type, Long userId);

    /** 标记单条为已读 */
    void markRead(Long id);

    /** 全部标记已读 */
    void markAllRead(Long userId);

    /** 未读消息数 */
    long unreadCount(Long userId);
}
