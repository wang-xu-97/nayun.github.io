document.addEventListener('DOMContentLoaded',  function() {
    const container = document.getElementById('tag-cloud'); 
    const tags = Array.from(container.querySelectorAll('.tag')); 
    
    // 计算最大和最小文章数量 
    const counts = tags.map(tag  => parseInt(tag.dataset.count)); 
    const minCount = Math.min(...counts); 
    const maxCount = Math.max(...counts); 
    
    // 计算最大和最小标签长度
    const lengths = tags.map(tag  => parseInt(tag.dataset.length)); 
    const minLength = Math.min(...lengths); 
    const maxLength = Math.max(...lengths); 
    
    // 排序标签：按文章数量降序
    tags.sort((a,  b) => {
      return parseInt(b.dataset.count)  - parseInt(a.dataset.count); 
    });
    
    // 创建分组容器 
    container.innerHTML  = '';
    const rowGroups = [
      {minWeight: 0.7, maxWeight: 1.0, rowClass: 'row-center', maxItems: 4},
      {minWeight: 0.4, maxWeight: 0.7, rowClass: 'row-middle', maxItems: 6},
      {minWeight: 0.0, maxWeight: 0.4, rowClass: 'row-outer', maxItems: 8}
    ];
    
    // 创建行容器
    rowGroups.forEach(group  => {
      const row = document.createElement('div'); 
      row.className  = `tag-row ${group.rowClass}`; 
      container.appendChild(row); 
    });
    
    // 计算标签尺寸并应用样式 
    tags.forEach(tag  => {
      // 根据标签长度计算字体大小
      const length = parseInt(tag.dataset.length); 
    //   const normalizedLength = (length - minLength) / (maxLength - minLength);
    //   const fontSize = 16 + normalizedLength * 16;
      const fontSize = 20;
      tag.style.fontSize  = `${fontSize}px`;
      
      // 根据权重计算颜色
      const count = parseInt(tag.dataset.count); 
      const normalizedCount = (count - minCount) / (maxCount - minCount);
      const hue = (normalizedCount * 120 + 200) % 360;
      tag.style.background  = `linear-gradient(135deg, hsl(${hue}, 70%, 50%), hsl(${(hue + 40) % 360}, 70%, 45%))`;
      
      // 临时添加到DOM以测量尺寸
      tag.style.position  = 'absolute';
      tag.style.left  = '-1000px';
      tag.style.top  = '0';
      document.body.appendChild(tag); 
      
      // 存储标签尺寸
      tag.dataset.width  = tag.offsetWidth; 
      tag.dataset.height  = tag.offsetHeight; 
      
      // 移除临时样式 
      tag.style.position  = '';
      tag.style.left  = '';
      tag.style.top  = '';
      document.body.removeChild(tag); 
    });
    
    // 将标签分配到合适的行
    const rows = container.querySelectorAll('.tag-row'); 
    
    tags.forEach(tag  => {
      const count = parseInt(tag.dataset.count); 
      const normalizedCount = (count - minCount) / (maxCount - minCount);
      
      let targetRow = null;
      
      // 确定标签所属行 
      for (let i = 0; i < rowGroups.length;  i++) {
        if (normalizedCount >= rowGroups[i].minWeight && normalizedCount <= rowGroups[i].maxWeight) {
          targetRow = rows[i];
          break;
        }
      }
      
      // 如果没找到合适的行，放在中间行
      if (!targetRow) {
        targetRow = rows[1];
      }
      
      targetRow.appendChild(tag); 
    });
    
    // 等分对齐算法 
    function layoutRows() {
      rows.forEach(row  => {
        const rowTags = Array.from(row.querySelectorAll('.tag')); 
        const rowWidth = row.offsetWidth; 
        
        if (rowTags.length  === 0) return;
        
        // 计算总宽度和间距
        const tagsWidth = rowTags.reduce((sum,  tag) => sum + parseFloat(tag.dataset.width),  0);
        const totalSpacing = rowWidth - tagsWidth;
        const spacing = totalSpacing / (rowTags.length  + 1);
        
        // 初始位置
        let currentX = spacing;
        
        // 设置每个标签位置 
        rowTags.forEach(tag  => {
          tag.style.position  = 'relative';
          tag.style.left  = '0';
          tag.style.top  = '0';
          tag.style.margin  = `0 ${spacing/2}px`;
          tag.style.transform  = 'none';
          currentX += parseFloat(tag.dataset.width)  + spacing;
        });
        
        // 设置行高度（根据行内最大标签高度）
        const maxHeight = Math.max(...rowTags.map(tag  => parseFloat(tag.dataset.height))); 
        row.style.minHeight  = `${maxHeight + 20}px`;
      });
    }
    
    // 初始布局
    layoutRows();
    
    // 添加点击动画
    tags.forEach(tag  => {
      tag.addEventListener('click',  function(e) {
        e.preventDefault(); 
        this.style.transform  = 'scale(0.95)';
        this.style.opacity  = '0.8';
        
        setTimeout(() => {
          window.location.href  = this.href; 
        }, 300);
      });
    });
    
    // 添加加载动画
    container.style.opacity  = '0';
    setTimeout(() => {
      container.style.transition  = 'opacity 0.8s ease';
      container.style.opacity  = '1';
    }, 200);
    
    // 窗口大小变化时重新布局 
    let resizeTimer;
    window.addEventListener('resize',  function() {
      clearTimeout(resizeTimer);
      
      // 添加过渡效果
      rows.forEach(row  => {
        row.style.transition  = 'all 0.4s ease';
        row.style.opacity  = '0.7';
      });
      
      resizeTimer = setTimeout(() => {
        layoutRows();
        rows.forEach(row  => {
          row.style.opacity  = '1';
        });
      }, 300);
    });
  });