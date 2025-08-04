document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.copy-button').forEach(button => {
      // 确保只创建一个提示元素
      if (!button.querySelector('.copy-tooltip')) {
        const tooltip = document.createElement('span');
        tooltip.className = 'copy-tooltip';
        tooltip.textContent = '✓ 已复制';
        button.appendChild(tooltip);
      }
      button.addEventListener('click', () => {
        const wrapper = button.closest('.code-block-wrapper');
        const codeBlock = wrapper.querySelector('pre code');
        const lines = Array.from(codeBlock.querySelectorAll('span:not(.ln)')); 
        const codeText = lines.map(line  => line.innerText).join('\n'); 
        const codeText1 = codeBlock.innerText;

        const codeLines = codeBlock.querySelectorAll('span.cl');
  
        // 提取每行的文本内容并拼接
        const codeText2 = Array.from(codeLines).map(line => {
            // 移除行号span及其后的空白（如果有）
            const lineClone = line.cloneNode(true);
            const lineNumber = lineClone.querySelector('span.ln');
            if (lineNumber) {
              lineNumber.remove();
            }
            // 获取纯文本并去除首尾空白
            return lineClone.textContent.replace(/\n+$/g,  '');
          })
          .join('\n'); // 用换行符连接各行

        const tooltip = button.querySelector('.copy-tooltip');
        
        // 临时保存按钮原始内容
        const originalHTML = button.innerHTML;
        
        const textarea = document.createElement('textarea');
        textarea.value = codeText2;
        document.body.appendChild(textarea);
        textarea.select();
        button.classList.add('hide-original');
        navigator.clipboard.writeText(textarea.value).then(() => {
        tooltip.style.opacity = '1';
        // 2秒后恢复按钮原始状态
        setTimeout(() => {
            tooltip.style.opacity = '0';
            button.classList.remove('hide-original');
        }, 2000);
        });
        
        document.body.removeChild(textarea);
      });
    });

    document.querySelectorAll('.language-label').forEach(button => {
      button.addEventListener('click', () => {
        const codeBlock = button.closest('.code-block-wrapper');
        const content = codeBlock?.querySelector('pre.chroma');
        if (content) content.classList.toggle('collapsed');
        else console.error('折叠失败');
      });
    });
});
