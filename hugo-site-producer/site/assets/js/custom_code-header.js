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
        const tooltip = button.querySelector('.copy-tooltip');
        
        // 临时保存按钮原始内容
        const originalHTML = button.innerHTML;
        
        const textarea = document.createElement('textarea');
        textarea.value = codeBlock.innerText;
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
    document.addEventListener('click', function(e) {
        if (e.target.closest('.fold-button')) {
            const button = e.target.closest('.fold-button');
            const codeBlock = button.closest('.code-block-wrapper');
            const content = codeBlock?.querySelector('.code-content');
            
            if (content) {
                content.classList.toggle('collapsed');
                
                const icon = button.querySelector('i');
                const textSpan = button.querySelector('span');
                
                if (content.classList.contains('collapsed')) {
                    icon?.classList.replace('fa-chevron-up', 'fa-chevron-down');
                    if (textSpan) textSpan.textContent = '展开';
                } else {
                    icon?.classList.replace('fa-chevron-down', 'fa-chevron-up');
                    if (textSpan) textSpan.textContent = '折叠';
                }
            }
        }
    });

    document.querySelectorAll('.language-label').forEach(button => {
      button.addEventListener('click', () => {
        const codeBlock = button.closest('.code-block-wrapper');
        const content = codeBlock?.querySelector('pre.chroma');
        if (content) {
            content.classList.toggle('collapsed');
            
        }
        else {
          console.error('折叠失败: ');
        }
        
      });
    });
  //   // 悬停效果增强 - 更健壮的实现
  //   document.querySelectorAll('.language-label').forEach(label => {
  //     const brackets = label.querySelector('.language-brackets');
  //     if (!brackets) return;
      
  //     label.addEventListener('mouseenter', () => {
  //         brackets.style.letterSpacing = '3px';
  //     });
      
  //     label.addEventListener('mouseleave', () => {
  //         brackets.style.letterSpacing = 'normal';
  //     });
  // });
});
