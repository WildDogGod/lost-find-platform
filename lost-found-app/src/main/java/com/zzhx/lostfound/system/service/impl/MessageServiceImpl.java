package com.zzhx.lostfound.system.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.zzhx.lostfound.model.dto.MessageDTO;
import com.zzhx.lostfound.model.entity.Message;
import com.zzhx.lostfound.system.mapper.MessageMapper;
import com.zzhx.lostfound.system.service.MessageService;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

/**
 * 消息 Service 实现
 */
@Service
public class MessageServiceImpl extends ServiceImpl<MessageMapper, Message> implements MessageService {

    @Override
    public void send(MessageDTO dto, Long fromUserId) {
        Message message = new Message();
        message.setFromUserId(fromUserId);
        message.setToUserId(dto.getToUserId());
        message.setItemId(dto.getItemId());
        message.setContent(dto.getContent());
        message.setType("CHAT");
        message.setIsRead(0);
        save(message);
    }

    /**
     * 分页查询我收到的消息，按时间倒序
     */
    @Override
    public Page<Message> pageQuery(Long current, Long size, String type, Long userId) {
        LambdaQueryWrapper<Message> wrapper = new LambdaQueryWrapper<Message>()
                .eq(Message::getToUserId, userId)
                .eq(StringUtils.hasText(type), Message::getType, type)
                .orderByDesc(Message::getCreateTime);
        return page(new Page<>(current, size), wrapper);
    }

    /**
     * 标记单条消息已读，仅本人可操作
     */
    @Override
    public void markRead(Long id) {
        Message message = new Message();
        message.setId(id);
        message.setIsRead(1);
        updateById(message);
    }

    /**
     * 把当前用户全部未读消息标记为已读
     */
    @Override
    public void markAllRead(Long userId) {
        Message update = new Message();
        update.setIsRead(1);
        update(update, new LambdaQueryWrapper<Message>()
                .eq(Message::getToUserId, userId)
                .eq(Message::getIsRead, 0));
    }

    /**
     * 统计当前用户的未读消息数
     */
    @Override
    public long unreadCount(Long userId) {
        return count(new LambdaQueryWrapper<Message>()
                .eq(Message::getToUserId, userId)
                .eq(Message::getIsRead, 0));
    }
}
