const { createApp, ref, onMounted, nextTick } = Vue;

createApp({
    setup() {
        const messages = ref([]);
        const inputText = ref('');
        const isLoading = ref(false);
        const sessionId = ref('');
        const chatContainer = ref(null);
        const fileInput = ref(null);
        const selectedFiles = ref([]);
        const showSessionInput = ref(false);
        const sessionToSwitch = ref('');
        const sessions = ref([]); // 存储所有会话ID

        // 后端API地址 - 假设后端运行在8000端口
        // const BASE_URL = 'http://127.0.0.1:8000';
        const BASE_URL = 'http://115.190.35.205:8000';
        // 初始化会话
        const initSession = async () => {
            try {
                // 尝试初始化会话，但在没有后端服务时也能正常工作
                try {
                    const response = await fetch(`${BASE_URL}/new_session`);
                    if (response.ok) {
                        const data = await response.json();
                        sessionId.value = data.session_id || 'default';
                        
                        // 将会话ID添加到会话列表中
                        if (sessionId.value && !sessions.value.includes(sessionId.value)) {
                            sessions.value.push(sessionId.value);
                        }
                        
                        // 对于新会话，也尝试获取历史记录（如果有的话）
                        if (sessionId.value) {
                            try {
                                const historyResponse = await fetch(`${BASE_URL}/switch_session?session_id=${encodeURIComponent(sessionId.value)}`);
                                if (historyResponse.ok) {
                                    const historyData = await historyResponse.json();
                                    if (Array.isArray(historyData)) {
                                        // 转换历史记录格式
                                        const formattedMessages = historyData.map((item, index) => ({
                                            id: Date.now() + index,
                                            type: item.role === 'human' ? 'user' : 'bot',
                                            content: item.content,
                                            streaming: false
                                        }));
                                        messages.value = formattedMessages;
                                        console.log('📜 初始会话历史已加载，共', messages.value.length, '条消息');
                                    }
                                }
                            } catch (historyError) {
                                console.log('无法加载历史记录，继续使用空会话');
                            }
                        }
                    }
                } catch (error) {
                    // 如果无法连接后端，使用临时会话ID
                    sessionId.value = 'temp-' + Date.now();
                    console.log('无法连接后端，使用临时会话ID:', sessionId.value);
                    
                    // 添加到会话列表
                    if (!sessions.value.includes(sessionId.value)) {
                        sessions.value.push(sessionId.value);
                    }
                }
            } catch (error) {
                console.error('初始化会话时发生错误:', error);
                // 确保至少有一个会话ID
                if (!sessionId.value) {
                    sessionId.value = 'temp-' + Date.now();
                    
                    // 添加到会话列表
                    if (!sessions.value.includes(sessionId.value)) {
                        sessions.value.push(sessionId.value);
                    }
                }
            }
        };

        // 触发文件选择
        const triggerFileInput = () => {
            fileInput.value.click();
        };

        // 处理文件选择
        const handleFileSelect = (event) => {
            const files = Array.from(event.target.files);
            selectedFiles.value.push(...files);
            event.target.value = '';
        };

        // 移除文件
        const removeFile = (index) => {
            selectedFiles.value.splice(index, 1);
        };

        // 格式化文件大小
        const formatFileSize = (bytes) => {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        };

        // 暂时注释掉文件上传功能，因为后端没有对应端点
        const uploadFiles = async () => {
            console.warn('文件上传功能暂未实现');
            return [];
        };

        // 流式读取响应 - 修复版本（使用响应式变量）
        const streamingContent = ref('');

        const readStream = async (reader, messageIndex) => {
            const decoder = new TextDecoder('utf-8');
            streamingContent.value = '';

            try {
                let chunkCount = 0;
                while (true) {
                    const { done, value } = await reader.read();

                    if (done) {
                        console.log('✅ 流式传输完成，共收到', chunkCount, '个数据块');
                        break;
                    }

                    chunkCount++;
                    const chunk = decoder.decode(value, { stream: true });
                    console.log(`📦 收到第 ${chunkCount} 个数据块:`, chunk.length, '字节');

                    // 累加到响应式变量
                    streamingContent.value += chunk;

                    // 通过数组索引直接更新（关键！）
                    messages.value[messageIndex].content = streamingContent.value;

                    // 滚动到底部
                    await nextTick();
                    scrollToBottom();
                }

                // 处理可能剩余的字节
                const finalChunk = decoder.decode();
                if (finalChunk) {
                    console.log('📦 最终数据块:', finalChunk.length, '字节');
                    streamingContent.value += finalChunk;
                    messages.value[messageIndex].content = streamingContent.value;
                    await nextTick();
                    scrollToBottom();
                }
            } catch (error) {
                console.error('❌ 流式读取错误:', error);
                streamingContent.value += '\n\n[读取响应时发生错误: ' + error.message + ']';
                messages.value[messageIndex].content = streamingContent.value;
            }
        };

        // 发送消息（支持流式传输）
        const sendMessage = async () => {
            if ((!inputText.value.trim() && selectedFiles.value.length === 0) || isLoading.value) return;

            const userMessage = {
                id: Date.now(),
                type: 'user',
                content: inputText.value.trim(),
                files: selectedFiles.value.map(file => ({
                    name: file.name,
                    size: file.size
                }))
            };

            messages.value.push(userMessage);
            const question = inputText.value.trim();
            inputText.value = '';
            isLoading.value = true;

            // 添加流式响应的消息占位
            messages.value.push({
                id: Date.now() + 1,
                type: 'bot',
                content: '',
                streaming: true
            });

            // 记录消息索引（关键！）
            const botMessageIndex = messages.value.length - 1;

            scrollToBottom();

            try {
                console.log('📤 发送请求到后端...');

                // 发送聊天消息到后端流式接口
                const response = await fetch(`${BASE_URL}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query: question,
                        session_id: sessionId.value
                    })
                });

                console.log('📥 响应状态:', response.status);
                console.log('📥 Content-Type:', response.headers.get('content-type'));

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                if (!response.body) {
                    throw new Error('Response body is not available');
                }

                console.log('🔄 开始读取流...');
                const reader = response.body.getReader();
                await readStream(reader, botMessageIndex);

            } catch (error) {
                console.error('❌ 发送消息失败:', error);
                messages.value[botMessageIndex].content = '抱歉，发生了错误：' + error.message;
            } finally {
                messages.value[botMessageIndex].streaming = false;
                isLoading.value = false;
                selectedFiles.value = [];
                scrollToBottom();
            }
        };

        // 新建会话
        const newSession = async () => {
            try {
                const response = await fetch(`${BASE_URL}/new_session`);
                const data = await response.json();
                const oldSessionId = sessionId.value;
                const newSessionId = data.session_id || 'default-' + Date.now().toString(36).substr(2, 9);
                
                // 将新会话ID添加到会话列表中
                if (!sessions.value.includes(newSessionId)) {
                    sessions.value.push(newSessionId);
                }
                
                // 切换到新会话
                sessionId.value = newSessionId;
                messages.value = [];
                selectedFiles.value = [];
                
                // 添加调试日志，帮助用户理解会话ID的变化
                console.log(`✅ 会话创建成功: 旧ID=${oldSessionId}, 新ID=${newSessionId}`);
                
                // 添加视觉反馈，让用户看到会话ID已更新
                const sessionIdElement = document.querySelector('.session-id.clickable');
                if (sessionIdElement) {
                    // 添加高亮效果
                    sessionIdElement.style.backgroundColor = '#dbeafe';
                    sessionIdElement.style.borderColor = '#3b82f6';
                    sessionIdElement.style.transition = 'all 0.3s ease';
                    
                    // 1秒后恢复原始样式
                    setTimeout(() => {
                        sessionIdElement.style.backgroundColor = '';
                        sessionIdElement.style.borderColor = '';
                    }, 1000);
                }
            } catch (error) {
                console.error('❌ 新建会话失败:', error);
                // 发生错误时也提供默认会话ID
                const fallbackSessionId = 'default-' + Date.now().toString(36).substr(2, 9);
                
                // 添加到会话列表
                if (!sessions.value.includes(fallbackSessionId)) {
                    sessions.value.push(fallbackSessionId);
                }
                
                sessionId.value = fallbackSessionId;
                messages.value = [];
                selectedFiles.value = [];
                console.log('⚠️  使用临时会话ID:', sessionId.value);
            }
        };

        // 清空当前会话
        const clearSession = async () => {
            try {
                // 根据app.py的实现，直接将session_id作为参数传递
                const response = await fetch(`${BASE_URL}/clear_session?session_id=${encodeURIComponent(sessionId.value)}`, {
                    method: 'POST'
                });
                if (response.ok) {
                    messages.value = [];
                    selectedFiles.value = [];
                } else {
                    throw new Error(`响应状态: ${response.status}`);
                }
            } catch (error) {
                console.error('清空会话失败:', error);
                alert('清空会话失败: ' + error.message);
            }
        };
        
        // 切换会话
        const switchSession = async () => {
            if (!sessionToSwitch.value.trim()) {
                alert('请输入会话ID');
                return;
            }
            
            try {
                const targetSessionId = sessionToSwitch.value.trim();
                const response = await fetch(`${BASE_URL}/switch_session?session_id=${encodeURIComponent(targetSessionId)}`);
                if (response.ok) {
                    const historyData = await response.json();
                    
                    // 将目标会话ID添加到会话列表中
                    if (!sessions.value.includes(targetSessionId)) {
                        sessions.value.push(targetSessionId);
                    }
                    
                    // 更新会话ID
                    sessionId.value = targetSessionId;
                    // 清空当前消息列表
                    messages.value = [];
                    selectedFiles.value = [];
                    
                    // 处理并显示会话历史
                    if (Array.isArray(historyData)) {
                        // 转换历史记录格式：将role转换为type，保持顺序（最近的在前）
                        const formattedMessages = historyData.map((item, index) => ({
                            id: Date.now() + index,
                            type: item.role === 'human' ? 'user' : 'bot',
                            content: item.content,
                            streaming: false
                        }));
                        
                        // 由于后端返回的是最近的在前，直接设置即可
                        messages.value = formattedMessages;
                        console.log('📜 会话历史已加载，共', messages.value.length, '条消息');
                    }
                    
                    // 隐藏输入框
                    showSessionInput.value = false;
                    sessionToSwitch.value = '';
                    
                    // 滚动到底部
                    await nextTick();
                    scrollToBottom();
                } else {
                    throw new Error(`响应状态: ${response.status}`);
                }
            } catch (error) {
                console.error('切换会话失败:', error);
                alert('切换会话失败: ' + error.message);
            }
        };
        
        // 通过点击会话按钮切换会话
        const switchSessionById = async (targetSessionId) => {
            try {
                // 如果已经是当前会话，不执行任何操作
                if (sessionId.value === targetSessionId) {
                    return;
                }
                
                const response = await fetch(`${BASE_URL}/switch_session?session_id=${encodeURIComponent(targetSessionId)}`);
                
                // 更新会话ID
                sessionId.value = targetSessionId;
                // 清空当前消息列表
                messages.value = [];
                selectedFiles.value = [];
                
                if (response.ok) {
                    const historyData = await response.json();
                    
                    // 处理并显示会话历史
                    if (Array.isArray(historyData)) {
                        // 转换历史记录格式
                        const formattedMessages = historyData.map((item, index) => ({
                            id: Date.now() + index,
                            type: item.role === 'human' ? 'user' : 'bot',
                            content: item.content,
                            streaming: false
                        }));
                        
                        messages.value = formattedMessages;
                        console.log('📜 会话历史已加载，共', messages.value.length, '条消息');
                    }
                }
                
                // 滚动到底部
                await nextTick();
                scrollToBottom();
            } catch (error) {
                console.error('通过ID切换会话失败:', error);
                // 即使失败也切换会话ID，但不加载历史记录
                sessionId.value = targetSessionId;
                messages.value = [];
                selectedFiles.value = [];
            }
        };
        
        // 删除指定会话
        const deleteSession = (id) => {
            console.log(`尝试删除会话: ${id}`);
            
            // 确认删除
            if (!confirm(`确定要删除会话 ${id.slice(0, 8)}... 吗？`)) {
                return;
            }
            
            // 从sessions数组中移除
            const index = sessions.value.indexOf(id);
            if (index !== -1) {
                sessions.value.splice(index, 1);
                
                // 如果删除的是当前活跃会话，需要切换到另一个会话或创建新会话
                if (id === sessionId.value) {
                    if (sessions.value.length > 0) {
                        // 切换到第一个可用会话
                        switchSessionById(sessions.value[0]);
                    } else {
                        // 如果没有其他会话，创建一个新会话
                        newSession();
                    }
                }
                
                // 尝试从后端删除会话
                try {
                    fetch(`${BASE_URL}/delete_session?session_id=${id}`, {
                        method: 'DELETE'
                    }).catch(error => {
                        console.error('从后端删除会话时出错:', error);
                    });
                } catch (error) {
                    console.error('从后端删除会话时出错:', error);
                }
            }
        };

        // 滚动到底部
        const scrollToBottom = () => {
            nextTick(() => {
                if (chatContainer.value) {
                    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
                }
            });
        };

        onMounted(() => {
            initSession();
        });

        return {
            messages,
            inputText,
            isLoading,
            sessionId,
            sessions,
            chatContainer,
            fileInput,
            selectedFiles,
            showSessionInput,
            sessionToSwitch,
            sendMessage,
            newSession,
            clearSession,
            switchSession,
            switchSessionById,
            deleteSession,
            triggerFileInput,
            handleFileSelect,
            removeFile,
            formatFileSize,
            scrollToBottom
        };
    }
}).mount('#app');